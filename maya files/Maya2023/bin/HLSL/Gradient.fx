
#include "Common.fxh"

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

// Vertex shader output structure.
struct VS_TO_PS_Gradient
{
    float4 HPos : POSITION;
    float3 Color : COLOR0;
};

// Vertex shader.
VS_TO_PS_Gradient VS_Gradient(VS_INPUT_ScreenQuad In)
{
    VS_TO_PS_Gradient Out;
    
    // Output the position directly.
    #ifdef FX_COMPOSER
        Out.HPos = float4(In.Pos, 1.0f);
    #else
        Out.HPos = mul(float4(In.Pos, 1.0f), gWVPXf);
    #endif

	// calculate vertex color
    Out.Color = lerp(gColor1, gColor2, In.UV.y);
    
    return Out;
}

// Pixel shader.
float4 PS_Gradient(VS_TO_PS_Gradient In) : COLOR0
{
    return float4(In.Color, 0.0f);
}

#ifndef FX_COMPOSER

// Main technique.
technique Main
{
    pass p0
    {
        VertexShader = compile vs_2_0 VS_Gradient();
        PixelShader = compile ps_2_0 PS_Gradient();
    }
}

#endif
