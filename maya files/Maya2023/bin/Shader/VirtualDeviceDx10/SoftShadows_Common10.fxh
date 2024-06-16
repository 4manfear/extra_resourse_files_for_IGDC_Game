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
// DESCRIPTION: Soft shadows - common definitions (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: November 2008
//**************************************************************************/

#ifndef _SOFTSHADOWS_COMMON_FXH_
#define _SOFTSHADOWS_COMMON_FXH_

// Whether an exponential warp should be applied to the depths in the shadow map, thus generating
// an exponential variance shadow map (EVSM) for reducing light bleeding.  For map sampling, this
// this means an exponential warp should be applied to the distance from the light.
// #define EVSM

#ifdef EVSM
    // The scales for the positive and negative exponential warps, for EVSM.
    float2 gExpFactor;
#endif

// World transformation.
float4x4 gWXf : World < string UIWidget = "None"; >;

// World-view-projection transformation.
// NOTE: For the shadow map pass, this contains the world-view-projection transformation from the
// perspective of the light of interest.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// Shadow map size and (internal) size of a texel in texel space.
int gShadowMapSize
<
    string UIName = "Shadow Map Size";
>
= 512;
static float gTexelSize = 1.0f / gShadowMapSize;

////////////////////////////////////////////////////////////////////////////////////////////////////
// Screen Quad Vertex Shader
////////////////////////////////////////////////////////////////////////////////////////////////////

// Vertex shader input structure.
struct VS_INPUT_ScreenQuad
{
    float3 Pos : POSITION;
    float2 UV : TEXCOORD0;
};

// Vertex shader output structure.
struct VS_TO_PS_ScreenQuad
{
    float4 HPos : SV_Position;
    float2 UV : TEXCOORD0;
};

// Vertex shader.
VS_TO_PS_ScreenQuad VS_ScreenQuad(VS_INPUT_ScreenQuad In)
{
    VS_TO_PS_ScreenQuad Out;
    
    // Output the position and texture coordinates directly.
    Out.HPos = mul(float4(In.Pos, 1.0f), gWVPXf);
    Out.UV = In.UV;
    
    return Out;
}

#endif // _SOFTSHADOWS_COMMON_FXH_