//**************************************************************************/
// Copyright (c) 2008 Autodesk, Inc.
// All rights reserved.
// 
// These coded instructions, statements, and computer programs contain
// unpublished proprietary information written by Autodesk, Inc., and are
// protected by Federal copyright law. They may not be disclosed to third
// parties or copied or duplicated in any form, in whole or in part, without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/
// DESCRIPTION: Screen space ambient occlusion - blur pass (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: October 2008
//**************************************************************************/

#include "SSAO_Common10.fxh"

// Specify a default blur amount (number of samples in each direction, or the "radius" of the box
// filter) if none is specified.  Use to determine the number of samples per pixel, including the
// center sample.
#ifndef BLUR_AMOUNT
    #define BLUR_AMOUNT 3
#endif
static int gNumSamples = BLUR_AMOUNT * 2 + 1;
static float2 gBlurRadius = BLUR_AMOUNT / gFullScreenSize;
static float2 gBlurRadiusTile = BLUR_AMOUNT / gScreenSize;
static float gCenterTap = BLUR_AMOUNT; // based on an iterator in the range [0, gNumSamples - 1]

#ifndef FX_COMPOSER

// The direction of the blur, e.g. (0.0, 1.0) for vertical.
float2 gBlurDirection < string UIWidget = "None"; > = { 1.0f, 0.0f };

// The source buffer and sampler.
Texture2D gSourceTex < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp;

// The depth buffer and sampler.
Texture2D gDepthTex < string UIWidget = "None"; > = NULL;
SamplerState gDepthSamp;

// The normal buffer and sampler.
Texture2D gNormalTex < string UIWidget = "None"; > = NULL;
SamplerState gNormalSamp;

#endif

// Pixel shader.
// NOTE: This expects screen quad vertex shader output.
float4 PS_SSAO_Blur(VS_TO_PS_ScreenQuad In,
    uniform Texture2D sourceTex, uniform SamplerState sourceSamp,
    uniform float2 direction) : SV_Target
{
    // Sample the normal and depth at the current pixel, and skip any background pixels, indicated
    // by a depth of zero.
    float depth = gDepthTex.SampleLevel(gDepthSamp, In.UV, 0);
    // if (depth <= 1e-10f) return sourceTex.SampleLevel(sourceSamp, In.UVTile, 0);

    // TODO: This is a workaround for a bug in the compiler for the D3D10 WARP renderer.  It can't
    // properly identify the shader as non-uniform because of the if statement above, which causes
    // the loop below to be incorrectly executed as uniform.  The workaround is to use an if / else
    // statement.  When this bug is fixed in the DX SDK, the original code above can be restored,
    // and the if / else can be removed.
    if (depth <= 1e-10f)
    {
        return sourceTex.SampleLevel(sourceSamp, In.UVTile, 0);
    }
    else
    {
        // Sample the normal.
        float3 normal = gNormalTex.SampleLevel(gNormalSamp, In.UV, 0).xyz * 2.0f - 1.0f;

        // Compute the sampling radius used at this depth in the SSAO pass.
        float2 depthScale = (gPerspectiveFlag ? depth : 1.0f) * gViewScale;
        float radius = gSampleRadius * (depthScale.x + depthScale.y); // * 0.5f * 2.0f = 1.0f
        
        // Compute the texel offset for each sample, and the location of the starting sample.
        // texture coordinates and offsets are needed when tiling is used: the depth buffer is the full
        // image size (UV) and the SSAO source buffer is tile size (UVTile).
        float2 offset = (direction * gBlurRadius) / BLUR_AMOUNT;
        float2 UV = In.UV - direction * gBlurRadius;
        float2 offsetTile = (direction * gBlurRadiusTile) / BLUR_AMOUNT;
        float2 UVTile = In.UVTile - direction * gBlurRadiusTile;
        
        // Perform a weighted blur that does not span large differences between depths.
        // NOTE: This is a technically a non-separable filter, but it provides reasonable results.
        float sum = 0.0f;
        float sumWeight = 0.0f;
        for (int i = 0; i < gNumSamples; i++)
        {
            // Sample the SSAO buffer and the depth buffer for the current sample.
            // NOTE: The SSAO buffer may only contain the content for a tile, so use the tile texture
            // coordinates.
            float value = sourceTex.SampleLevel(sourceSamp, UVTile, 0);
            float valueDepth = gDepthTex.SampleLevel(gDepthSamp, UV, 0);
            float3 valueNormal = gNormalTex.SampleLevel(gNormalSamp, UV, 0).xyz * 2.0f - 1.0f;
            
            // Compute the difference in depth and the dot product between the normals.
            float depthDiff = abs(valueDepth - depth);
            float normalDot = dot(valueNormal, normal);
         
            // Add the sample to the sum if the depth difference is small or the dot product is near one.
            if (depthDiff < radius * 0.25f && (/*normalDot < 1e-4f || */ normalDot > 0.9f))
            {
                // Apply a Bartlett triangular filter kernel from 0.2 at the outer samples to 1.0 in the
                // center.
                // NOTE: This differs from the original OGS version, which just performs a box blur.
                const float wMin = 0.2f;
                float w = (1.0f - wMin) * (1.0f - abs(1.0f - i / gCenterTap)) + wMin;
                sum += value * w;
                sumWeight += w;
            }

            // Increment the texture coordinates by the offset.
            UV += offset;
            UVTile += offsetTile;
        }
        
        // Take a weighted average of the values.
        sum /= sumWeight;
        
        // Return the weighted average as the grayscale color output of the shader.
        return float4(sum.xxx, 1.0f);
    }
}

#ifndef FX_COMPOSER

// Technique.
technique10 SSAO_Blur
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_SSAO_Blur(gSourceTex, gSourceSamp, gBlurDirection)));
    }
}

#endif
