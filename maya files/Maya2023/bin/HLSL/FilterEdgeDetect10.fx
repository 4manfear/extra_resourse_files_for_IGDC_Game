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
float gThickness 
<
    string UIName = "Thickness";
    string UIWidget = "slider";
    float UIMin = 1.0f;
    float UIMax = 5.0f;
    float UIStep = 0.5f;
> = 1.5f;

// The edge detection threshold.
float gThreshold
<
    string UIName = "Threshold";
    string UIWidget = "slider";
    float UIMin = 0.01f;
    float UIMax = 0.5f;
    float UIStep = 0.01f;
> = 0.2;

// Gets the grayscale value of a color, i.e. the average of the RGB components.
float GetGray(float4 c)
{
    return dot(c.rgb, (0.33333).xxx);
}

// Pixel shader.
float4 PS_FilterEdgeDetect(VS_TO_PS_ScreenQuad In) : SV_TARGET
{
    float2 ox = float2(gThickness/gTargetSize.x,0.0);
    float2 oy = float2(0.0,gThickness/gTargetSize.y);
    float2 uv = In.UV.xy;
    float2 PP = uv - oy;
    float4 CC = gInputTex.Sample(gInputSampler,PP-ox); float g00 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP);    float g01 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP+ox); float g02 = GetGray(CC);
    PP = uv;
    CC = gInputTex.Sample(gInputSampler,PP-ox); float g10 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP);    float g11 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP+ox); float g12 = GetGray(CC);
    PP = uv + oy;
    CC = gInputTex.Sample(gInputSampler,PP-ox); float g20 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP);    float g21 = GetGray(CC);
    CC = gInputTex.Sample(gInputSampler,PP+ox); float g22 = GetGray(CC);
    float K00 = -1;
    float K01 = -2;
    float K02 = -1;
    float K10 = 0;
    float K11 = 0;
    float K12 = 0;
    float K20 = 1;
    float K21 = 2;
    float K22 = 1;
    float sx = 0;
    float sy = 0;
    sx += g00 * K00;
    sx += g01 * K01;
    sx += g02 * K02;
    sx += g10 * K10;
    sx += g11 * K11;
    sx += g12 * K12;
    sx += g20 * K20;
    sx += g21 * K21;
    sx += g22 * K22; 
    sy += g00 * K00;
    sy += g01 * K10;
    sy += g02 * K20;
    sy += g10 * K01;
    sy += g11 * K11;
    sy += g12 * K21;
    sy += g20 * K02;
    sy += g21 * K12;
    sy += g22 * K22; 
    float dist = sqrt(sx*sx+sy*sy);
	// black outline
    if (dist > gThreshold) 
	{ 
		return float4(0,0,0,1);
	}
	return gInputTex.Sample(gInputSampler, uv);
}

// The main technique.
technique10 Main
{
   pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_FilterEdgeDetect()));
    }
}

