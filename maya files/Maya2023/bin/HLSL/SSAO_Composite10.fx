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
// DESCRIPTION: Screen space ambient occlusion - composite pass (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: October 2008
//**************************************************************************/

#include "SSAO_Common10.fxh"

// Whether to composite with a scene buffer.  When this is not enabled, blending state should be
// enabled as desired to composite with an existing target, rather than using a previously
// rendered target (i.e. the scene buffer).
// #define USE_SCENE_BUFFER

// The SSAO composite factor.
float gCompositeFactor
<
    string UIName = "Composite Factor";
    string UIWidget = "Slider";
    float UIMin = 0.0f;
    float UIMax = 1.0f;
    float UIStep = 0.1f;
> = 1.0f;

// The SSAO composite color (tint).
float3 gCompositeColor
<
    string UIName = "Composite Color";
    string UIWidget = "Color";
> = float3(0.0f, 0.0f, 0.0f);

#ifndef FX_COMPOSER

// The source buffer and sampler.
Texture2D gSourceTex < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp;

#ifdef USE_SCENE_BUFFER
	// The scene buffer and sampler.
	Texture2D gSceneTex < string UIWidget = "None"; > = NULL;
	SamplerState gSceneSamp;
#endif

#endif

// Pixel shader.
// NOTE: This expects screen quad vertex shader output.
float4 PS_SSAO_Composite(VS_TO_PS_ScreenQuad In,
	uniform Texture2D sourceTex, uniform SamplerState sourceSamp) : SV_Target
{
	/// Compute the SSAO "intensity" as a linear interpolation between 1.0 (no SSAO) and the pixel
    // from the SSAO buffer, based on the composite factor.  The composite factor can exceed 1.0
    // to increase the SSAO effect.
    float source = sourceTex.Sample(sourceSamp, In.UVTile).r;
    float intensity = saturate(lerp(1.0f, source, 2.0f * gCompositeFactor));
    
    #ifdef USE_SCENE_BUFFER
        // Compute a tint color from the composite color and the intensity, and return the tint
        // color multiplied by the sceen buffer color, and the scene buffer alpha.
		float4 scene = gSceneTex.Sample(gSceneSamp, In.UVTile);
        float3 tint = lerp(gCompositeColor, 1.0f, intensity);
        return float4(tint * scene.rgb, scene.a);
	#else
        // Return the intensity as the composite color with alpha set to the intensity.
        return float4(gCompositeColor, intensity);
	#endif
}

#ifndef FX_COMPOSER

// Technique.
technique10 SSAO_Composite
{
    pass p0
    {
		SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
    	SetGeometryShader(NULL);
    	SetPixelShader(CompileShader(ps_4_0, PS_SSAO_Composite(gSourceTex, gSourceSamp)));
    }
}

#endif
