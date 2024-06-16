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
// DESCRIPTION: Soft shadows - shadow map.
// AUTHOR: Mauricio Vives
// CREATED: January 2009
//**************************************************************************/

#include "SoftShadows_Common.fxh"

#ifndef FX_COMPOSER

// Depth map texture and sampler.
texture2D gDepthMapTex < string UIWidget = "None"; > = NULL;
sampler2D gDepthMapSamp = sampler_state
{
    texture = <gDepthMapTex>;
};

#endif

// Pixel shader.
float4 PS_ShadowMap(VS_TO_PS_ScreenQuad In) : COLOR0
{
    // Get the depth from the depth map.
    float depth = tex2D(gDepthMapSamp, In.UV).r;

    float4 result = 0.0f;

#ifdef EVSM
    // Compute values to form an exponential variance shadow map (EVSM):
    // X/Y: The depth with a positive exponential warp applied to it, and that value squared.
    // Z/W: The depth with a negative exponential warp applied to it, and that value squared.
    result.x =  exp( gExpFactor.x * depth);
    result.y = result.x * result.x;
    result.z = -exp(-gExpFactor.y * depth);
    result.w = result.z * result.z;
#else
    // Use the depth and depth-squared to form a standard variance shadow map (VSM).
    result.x = depth;
    result.y = result.x * result.x;
#endif

    return result;
}

#ifndef FX_COMPOSER

// Technique.
technique ShadowMap_Main
{
    pass p0
    {
        VertexShader = compile vs_2_0 VS_ScreenQuad();
        PixelShader = compile ps_2_0 PS_ShadowMap();
    }
}

#endif