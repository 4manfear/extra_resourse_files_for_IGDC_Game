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
// DESCRIPTION: IBL Generation : render result to another target.
// AUTHOR: Liming Zhang
// CREATED: June 2011
//**************************************************************************/

// World-view-projection transformation.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// The input texture.
texture2D gColorTex : InputTexture
<
    string UIName = "Input Texture";
> = NULL;

// The input sampler.
sampler gColorSamp = sampler_state 
{
    Texture   = <gColorTex>;
};


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
};

// Vertex shader.
VS_TO_PS VS_CopyResult(VS_INPUT In)
{
    VS_TO_PS Out;
    
    // Transform the position from object space to clip space for output.
    Out.HPos = mul(In.Pos, gWVPXf);
    
    // Pass the texture coordinates unchanged.
    Out.UV = In.UV;
    
    return Out;
}


// Pixel shader.
float4 PS_CopyResult(VS_TO_PS In) : COLOR
{
    // A simple calculation.
    float4 result = tex2D(gColorSamp, In.UV);
    return result / result.w;
}

// The main technique.
technique Main
{
    pass p0
    {
        VertexShader = compile vs_2_0 VS_CopyResult();
        PixelShader = compile ps_2_0 PS_CopyResult();
    }
}
