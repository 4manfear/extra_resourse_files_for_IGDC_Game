//**************************************************************************/
// Copyright 2011 Autodesk, Inc.
// All rights reserved.
//
// This computer source code and related instructions and comments are the
// unpublished confidential and proprietary information of Autodesk, Inc.
// and are protected under Federal copyright and state trade secret law.
// They may not be disclosed to, copied or used by any third party without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/
// DESCRIPTION: Sum pixel values.
// AUTHOR: Liming Zhang
// CREATED: Mar. 2011
//**************************************************************************/

// World-view-projection transformation.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// The input direction texture.
texture gSumTexture : InputTexture
<
    string UIName = "Input Texture";
> = NULL;

// Filter input sampler.
sampler2D gSumSamp = sampler_state 
{
    Texture   = <gSumTexture>;
};

// Pixel size. 
float2 gPixelSize;

// Vertex shader input structure.
struct VS_INPUT
{
    float4 Pos : POSITION;
    float2 UV : TEXCOORD0;
};

// Vertex shader output structure.
struct VS_TO_PS
{
    float4 HPos : POSITION;
    float2 UV : TEXCOORD0;
    float2 OffsetCoords0 : TEXCOORD1;
    float2 OffsetCoords1 : TEXCOORD2;
    float2 OffsetCoords2 : TEXCOORD3;
    float2 OffsetCoords3 : TEXCOORD4;
};

// Vertex shader.
VS_TO_PS VS_SumPixelValues(VS_INPUT In)
{
    VS_TO_PS Out;
    
    // Transform the position from object space to clip space for output.
    Out.HPos = mul(In.Pos, gWVPXf);
    
    // Pass the texture coordinates unchanged.
    Out.UV = In.UV;
    
    float2 offset = gPixelSize * 0.25;

    Out.OffsetCoords0 = In.UV + float2(offset.x, offset.y);
    Out.OffsetCoords1 = In.UV + float2(offset.x, -offset.y);
    Out.OffsetCoords2 = In.UV + float2(-offset.x, -offset.y);
    Out.OffsetCoords3 = In.UV + float2(-offset.x, offset.y);

    return Out;
}

// Pixel shader.
float4 PS_SumPixelValues(VS_TO_PS In) : COLOR
{
    float4 result = 0.0f; 
    result += tex2D(gSumSamp, In.OffsetCoords0);
    result += tex2D(gSumSamp, In.OffsetCoords1);
    result += tex2D(gSumSamp, In.OffsetCoords2);
    result += tex2D(gSumSamp, In.OffsetCoords3);
    return result;
}

// The main technique.
technique Main
{
    pass p0
    {
        VertexShader = compile vs_2_0 VS_SumPixelValues();
        PixelShader = compile ps_2_0 PS_SumPixelValues();
    }
}
