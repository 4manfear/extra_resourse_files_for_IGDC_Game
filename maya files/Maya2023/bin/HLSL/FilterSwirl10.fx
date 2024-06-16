
//**************************************************************************/
// Copyright 2015 Autodesk, Inc.
// All rights reserved.
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//**************************************************************************/
#include "Common10.fxh"

// Target size.
float2 gTargetSize : ViewportPixelSize < string UIWidget = "None"; >;

Texture2D gInputTex;
SamplerState gInputSampler;

// Swirl options
float radius = 300.0;
float angle = 0.8;
float2 centerPercent = { 0.5, 0.5 };

// Pixel shader.
float4 PS_FilterSwirl(VS_TO_PS_ScreenQuad In) : SV_TARGET
{
	float2 uv = In.UV.xy;

	float2 center = gTargetSize * centerPercent;
	float2 tc = uv * gTargetSize;
	tc -= center;
	float dist = length(tc);
	if (dist < radius) 
	{
		float percent = (radius - dist) / radius;
		float theta = percent * percent * angle * 8.0;
		float s = sin(theta);
		float c = cos(theta);
		tc = float2(dot(tc, float2(c, -s)), dot(tc, float2(s, c)));
	}
	tc += center;
	float3 color = gInputTex.Sample(gInputSampler, tc / gTargetSize).rgb;
	return float4(color, 1.0);	
}

// The main technique.
technique10 Main
{
    pass p0
    {
		SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_FilterSwirl()));
    }
}
