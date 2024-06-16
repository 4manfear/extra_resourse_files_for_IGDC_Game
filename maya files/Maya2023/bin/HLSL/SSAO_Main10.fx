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
// DESCRIPTION: Screen space ambient occlusion - main pass (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: October 2008
//**************************************************************************/

#include "SSAO_Common10.fxh"
#include "SSAO_Samples10.fxh"

// Define this macro to use a second depth layer, for allowing hidden surfaces (the back faces)
// to contribute to the SSAO result.
// #define DOUBLE_LAYER

// The number of SSAO samples to use, between 1 and 64.
#ifndef NUM_SAMPLES
    #define NUM_SAMPLES 16
#endif

// The random normalized vector texture.
// NOTE: This is assumed to be 8x8 in an unsigned format.
Texture2D gRandomTex
<
    string UIName = "Random Texture";
    string ResourceName = "RandomVector.bmp";
> = NULL;

// The random texture sampler.
SamplerState gRandomSamp
{
    #ifdef FX_COMPOSER
        AddressU = Wrap;
        AddressV = Wrap;
        Filter = MIN_MAG_MIP_POINT;
    #endif
};

bool MayaHwFogEnabled : fogEnabled < string UIWidget = "None"; > = false;
int MayaHwFogMode : fogMode < string UIWidget = "None"; > = 0;
float MayaHwFogStart : fogStart < string UIWidget = "None"; > = 0.0f;
float MayaHwFogEnd : fogEnd < string UIWidget = "None"; > = 100.0f;
float MayaHwFogDensity : fogDensity < string UIWidget = "None"; > = 0.1f;
float4 MayaHwFogColor : fogColor < string UIWidget = "None"; > = { 0.5f, 0.5f, 0.5f , 1.0f };

#ifndef FX_COMPOSER

// The normal and depth buffers and samplers.
Texture2D gNormalTex < string UIWidget = "None"; > = NULL;
SamplerState gNormalSamp;
Texture2D gDepthTex < string UIWidget = "None"; > = NULL;
SamplerState gDepthSamp;

#ifdef DOUBLE_LAYER
// The second layer depth buffer and sampler.
Texture2D gDepthTex2 < string UIWidget = "None"; > = NULL;
SamplerState gDepthSamp2;
#endif

#endif

// Pixel shader.
// NOTE: This expects screen quad vertex shader output.
float4 PS_SSAO_Main(VS_TO_PS_ScreenQuad In) : SV_Target
{
    // Get the depth of the current pixel.
    float depth = gDepthTex.SampleLevel(gDepthSamp, In.UV, 0).x;

    // Return white if the depth is less than or equal to zero.  This indicates the background,
    // which does not need any SSAO processing.
    if (depth <= 1e-10f) return 1.0f;
    
    // Compute the depth scale from the depth of the current pixel and the view scale.  This
    // is the vector from the center of the screen to the corners of the screen in view space, at
    // the current depth.  This is used to convert the screen-space sampling radius (i.e. a fraction
    // of the screen width and height) to a view-space radius.
    // NOTE: The average of the depth scale x and y components are used.  Multiplying by 1/2 to
    // compute the average cancels out multiplying by 2 to convert the depth scale from half the
    // view (center to edge) to the full view, so that is left commented out.
    float2 depthScale = (gPerspectiveFlag ? depth : 1.0f) * gViewScale;
    float radius = gSampleRadius * (depthScale.x + depthScale.y); // * 0.5f * 2.0f = 1.0f
    
    // Reconstruct the view-space (3D) position of the current pixel from the depth, the depth
    // scale, and the normalized [0.0, 1.0] screen position.
    float2 pos2D = In.UV * float2(2.0f, -2.0f) + float2(-1.0f, 1.0f);
    float3 pos3D = float3(pos2D * depthScale, depth);

    // Sample the random texture to get a random normalized vector, based on the current screen
    // position.  The texture is assumed to have the wrap addressing mode, have 8x8 dimensions,
    // and have an unsigned type (e.g. 32-bit RGBA).  The vector components must be scaled and
    // translated from unsigned values to signed values (i.e. times-two-minus-one).
    float3 random = gRandomTex.SampleLevel(gRandomSamp, In.UV * gFullScreenSize / 8.0f, 0).xyz * 2.0f - 1.0f;
    
    // Get the normal of the current pixel.
    float3 normal = gNormalTex.SampleLevel(gNormalSamp, In.UV, 0).xyz * 2.0f - 1.0f;

    // Iterate the indicated number of samples to compute the total visibility contribution of the
    // samples.  The "sum" variable is a measure of visibility, the opposite of occlusion.
    float sum = 0.0f;
    for (int i = 0; i < NUM_SAMPLES; i++)
    {
        // Get an offset from the offset array, which contains a set of random points inside a unit
        // sphere.  The offset is reflected by the per-pixel random vector, to replace banding
        // artifacts with (less objectionable) noise instead.  The reflected offset is then negated
        // if is on the opposite side of the surface normal, so that all sample points are on the
        // same side as the normal, i.e. a hemisphere of offsets instead of a sphere.  The offset
        // is then added to the 3D pixel position to create a 3D sample point.
        float3 offset = reflect( GetOffset(i), random);
        if (dot(offset, normal) < 0.0f) offset = -offset;
        float3 sample3D = pos3D + offset * radius;
        
        // Project the 3D sample point to NDC space, by dividing by the depth scale of the sample
        // point.  Note that the depth scale of the sample point will differ slightly from the depth
        // scale computed above for the pixel position.  Only the 2D NDC components are needed.
        float2 sampleNDC = sample3D.xy / ((gPerspectiveFlag ? sample3D.z : 1.0f) * gViewScale);
        
        // Compute the UV coordinates of the NDC-space sample point (relative to the screen quad),
        // and sample the depth buffer.
        float2 sampleUV = float2(0.5f, -0.5f) * sampleNDC + float2(0.5f, 0.5f);
        float sampleDepth = gDepthTex.SampleLevel(gDepthSamp, sampleUV, 0).x;

        // Compute the difference in depth between the sample point and the depth in the buffer,
        // If the occluder is behind the sample point, use full visibility for this sample.
        // Otherwise compute visibility based on the distance to the occluder.  Do nothing if the
        // original sample depth is less than or equal to zero.
        float vis1 = 1.0f;
        float diff = max(sample3D.z - sampleDepth, 0.0f);
        if (sampleDepth > 0.0f)
        {
            // Reduce visibility based on the computed difference, normalized to the sampling
            // radius, with non-linear attenuation.  The greater the distance, the more occlusion.
            vis1 = diff > radius ? 1.0f : pow(1.0f - diff / radius, 2);

            // A more complex alternative, to be executed only if diff > 0.0:
            // Compute the distance between the 3D pixel position and the 3D position at the sampled
            // depth.  If this is larger than the sampling radius, use full visibility.  Otherwise,
            // compute the occlusion based on the normalized distance, i.e. relative to the sampling
            // radius.  A larger distance means a farther occluder, and thus more visibility.
            //
            // float dist = length(float3(sample3D.xy, sampleDepth) - pos3D);
            // vis1 = min(pow(dist / radius, 2), 1.0f);
        }
        
#ifdef DOUBLE_LAYER
        // Repeat for the back faces, using the second normal-depth buffer.
        float vis2 = 1.0f;
        sampleDepth = gDepthTex2.SampleLevel(gDepthSamp2,  sampleUV, 0);
        diff = max(sample3D.z - sampleDepth, 0.0f);
        if (sampleDepth > 0.0f && diff > 0.0f)
        {
            vis2 = diff > radius ? 1.0f : pow(1.0f - diff / radius, 2);
        }
        
        // Select the value with the least visibility, and add it to the sum.
        sum += min(vis1, vis2);
#else
        sum += vis1;
#endif
    }
    
	// Compute the average visibility from the samples.
    float average = sum / NUM_SAMPLES;
	
	if (MayaHwFogEnabled) {
		float fogFactor = 0.0f;
		if (MayaHwFogMode == 0) {
			fogFactor = saturate((MayaHwFogEnd - depth) / (MayaHwFogEnd - MayaHwFogStart));
		}
		else if (MayaHwFogMode == 1) {
			fogFactor = rcp(exp(depth * MayaHwFogDensity));
		}
		else if (MayaHwFogMode == 2) {
			fogFactor = rcp(exp(pow(depth * MayaHwFogDensity, 2)));
		}
		fogFactor = (1.0f - fogFactor) * MayaHwFogColor.a;
		average =  lerp(average, 1, fogFactor);		
	}
	
    // Return the average visibility as the grayscale color output of the shader.
    return float4(average.xxx, 1.0f);
}

#ifndef FX_COMPOSER

// Technique.
technique10 SSAO_Main
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_SSAO_Main()));
    }
}

#endif