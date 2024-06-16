//**************************************************************************/
// Copyright 2011 Autodesk, Inc.  
// All rights reserved.
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form.   
//**************************************************************************/

#include "Common10.fxh"

// Top color.
float3 gColor1
<
    string UIName = "Color1 (top)";
    string UIWidget = "Color";
> = { 1.0f, 0.0f, 0.0f };

// Bottom color.
float3 gColor2
<
    string UIName = "Color2 (bottom)";
    string UIWidget = "Color";
> = { 0.0f, 0.0f, 1.0f };

// Pixel shader.
float4 PS_Gradient(VS_TO_PS_ScreenQuad In) : SV_Target
{
    float3 color = lerp(gColor1, gColor2, In.UV.y);
	return float4(color, 0.0);
}

#ifndef FX_COMPOSER

// Main technique.
technique10 Main
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_Gradient()));
	}
}

#endif
