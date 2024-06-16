//**************************************************************************/
// Copyright 2011 Autodesk, Inc.  
// All rights reserved.
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form.   
//**************************************************************************/

#include "Common10.fxh"

// Specify a default blur amount (number of samples in each direction, or the "radius" of the box
// filter) if none is specified.  Use to determine the number of samples per pixel, including the
// center sample.
// NOTE: This can have a maximum value of 12 to work within SM2.
#ifndef BLUR_AMOUNT
    #define BLUR_AMOUNT 5
#endif
static int gNumSamples = BLUR_AMOUNT * 2 + 1;

#ifndef FX_COMPOSER

// The source buffer and sampler.
Texture2D gSourceTex < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp;

#endif

float4 gUVTransform : RelativeViewportDimensions;

// Pixel shader.
// NOTE: This expects screen quad vertex shader output.
float4 PS_Blur(VS_TO_PS_ScreenQuad In,
    uniform Texture2D sourceTex, uniform SamplerState sourceSamp,
    uniform float2 direction) : SV_Target
{
    // Compute the per-sample offset, based on the texel size and blur direction.  Then compute the
    // location of the starting sample, using the number of taps.
    float2 offset = direction * gTexelSize;
    float2 UV = In.UV * gUVTransform.zw + gUVTransform.xy - offset * (gNumSamples - 1) * 0.5f;
    
    // Sum each of the samples (box filter).
    float4 sum = 0;
    for (int i = 0; i < gNumSamples; i++)
    {
        // Add the value from the source texture.
        sum += sourceTex.Sample(sourceSamp, UV);
        
        // Increment the texture coordinates by the offset.
        UV += offset;
    }
    
    // Return the average color and alpha.
    return float4(sum / gNumSamples);
}

#ifndef FX_COMPOSER

// Horizontal blur technique.
technique10 BlurHoriz
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_Blur(gSourceTex, gSourceSamp, float2(1.0f, 0.0f))));
        // A horizontal blur direction is specified as an argument above.
    }
}

// Vertical blur technique.
technique10 BlurVert
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_Blur(gSourceTex, gSourceSamp, float2(0.0f, 1.0f))));
        // A vertical blur direction is specified as an argument above.
    }
}

#endif