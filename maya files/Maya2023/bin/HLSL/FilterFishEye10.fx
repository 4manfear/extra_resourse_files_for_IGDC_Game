
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

// The edge thickness.
float aperture 
<
    string UIName = "Aperture";
    string UIWidget = "slider";
    float UIMin = 1.0f;
    float UIMax = 180.0f;
    float UIStep = 1.0f;
> = 178.0;

// Pixel shader.
float4 PS_FilterFishEye(VS_TO_PS_ScreenQuad In) : SV_TARGET
{
	float apertureHalf = 0.5 * aperture * (3.1415926535 / 180.0);
	float maxFactor = sin(apertureHalf);

	float2 uv;
	float2 xy = 2.0 * In.UV.xy - 1.0;
	float d = length(xy);
	if (d < (2.0-maxFactor))
	{
		d = length(xy * maxFactor);
		float z = sqrt(1.0 - d * d);
		float r = atan2(d, z) / 3.1415926535;
		float phi = atan2(xy.y, xy.x);

		uv.x = r * cos(phi) + 0.5;
		uv.y = r * sin(phi) + 0.5;
	}
	else
	{
		uv = In.UV.xy;
	}
	float4 c = gInputTex.Sample(gInputSampler, uv);
	return c;
}

// The main technique.
technique10 Main
{
    pass p0
    {
		SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_FilterFishEye()));
    }
}
