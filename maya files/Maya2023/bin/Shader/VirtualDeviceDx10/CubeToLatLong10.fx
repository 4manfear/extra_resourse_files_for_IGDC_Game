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
// DESCRIPTION: Sample a cube texture and render it to a Lat-Long texture.
// AUTHOR: Liming Zhang
// CREATED: Mar. 2011
//**************************************************************************/

// World-view-projection transformation.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// The input direction texture.
texture2D gDirectionTex : InputTexture
<
    string UIName = "Input Texture";
> = NULL;

// Direction texture sampler.
sampler DirectionSamp = sampler_state 
{
    Texture   = <gDirectionTex>;
};


// The input HDR cube texture.
TextureCube gHDRCubeTex : InputTexture
<
    string UIName = "Input Texture";
> = NULL;

// Cube texture sampler.
sampler HDRCubeSamp = sampler_state 
{
    Texture   = <gHDRCubeTex>;
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
    float4 HPos : SV_Position;
    float2 UV : TEXCOORD0;
};

// Vertex shader.
VS_TO_PS VS_CubeToLatLong(VS_INPUT In)
{
    VS_TO_PS Out;
    
    // Transform the position from object space to clip space for output.
    Out.HPos = mul(In.Pos, gWVPXf);
    
    // Pass the texture coordinates unchanged.
    Out.UV = In.UV;
    
    return Out;
}

// Pixel shader.
float4 PS_CubeToLatLong(VS_TO_PS In) : SV_Target
{
    // Translate UV to direction by sampling Direction texture.
    float3 dir = gDirectionTex.Sample(DirectionSamp, In.UV).rgb;

    // Sample the HDR cube map.
    float3 color = gHDRCubeTex.Sample(HDRCubeSamp, dir).rgb;

    return float4( color, 1.0);
}

// The main technique.
technique10 Main
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_CubeToLatLong()));
        SetPixelShader(CompileShader(ps_4_0, PS_CubeToLatLong()));
    }
}
