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
// DESCRIPTION: Screen space ambient occlusion - normal-depth buffer pass (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: October 2008
//**************************************************************************/

#include "SSAO_Common10.fxh"
#ifdef CLIPPING // D3D10 ONLY
#include "Clipping10.fxh"
#endif

// Check if the back-facing normal need to be flipped.
extern bool isSingleSided = false;
extern float mayaNormalMultiplier = 1.0f;

// Whether the projection matrix flips Z: -1.0 if so, otherwise 1.0.
#ifdef FX_COMPOSER
    float gProjZSense < string UIWidget = "None"; > = -1.0f;
#else
    float gProjZSense : ProjectionZSense < string UIWidget = "None"; >;
#endif

// Vertex shader input structure.
struct VS_INPUT_NormalDepth
{
    float3 Pos : POSITION;
    float3 Normal: NORMAL;
};

// Vertex shader output structure.
struct VS_TO_PS_NormalDepth
{
    float4 HPos : SV_Position;
    float4 NormalDepth : TEXCOORD0;
    
    #ifdef CLIPPING // D3D10 ONLY
        // Clip distances, for eight clipping planes.
        float4 ClipDistances0 : SV_ClipDistance0;
        float4 ClipDistances1 : SV_ClipDistance1;
    #endif

};

// Vertex shader.
VS_TO_PS_NormalDepth VS_NormalDepth(VS_INPUT_NormalDepth In)
{
    VS_TO_PS_NormalDepth Out;
    
    // Transform the vertex from object space to clip space.
    Out.HPos = mul(float4(In.Pos, 1.0f), gWVPXf);
    
    // Record the normal and depth components for the pixel shader.
    // NOTE: This depends on whether the view direction is along +Z or -Z.  The projection matrix
    // "Z sense" determines this.
    Out.NormalDepth.xyz = mul(In.Normal, gWVITXf);
    Out.NormalDepth.z = gProjZSense * Out.NormalDepth.z;
    Out.NormalDepth.w = gProjZSense * mul(float4(In.Pos, 1.0f), gWVXf).z;

    #ifdef CLIPPING // D3D10 ONLY
        // Compute the eight clip distances.
        float4 HPw = mul(float4(In.Pos, 1.0f), gWXf);
        ComputeClipDistances(HPw, Out.ClipDistances0, Out.ClipDistances1);
    #endif

    return Out;
}

// Pixel shader output structure.
struct PS_OUT
{
    float4 Normal : SV_Target0;
    float4 Depth : SV_Target1;
};

// Pixel shader.
PS_OUT PS_NormalDepth(VS_TO_PS_NormalDepth In, bool isFrontFace : SV_IsFrontFace)
{
    PS_OUT Out;
	
	float3 normal = normalize(In.NormalDepth.xyz);

	if ( !isSingleSided )
	{
		float normalMul = isFrontFace ? mayaNormalMultiplier : -mayaNormalMultiplier;
		normal *= normalMul;
	}

    // Set the normal for an unsigned normalized integer target, and depth for a floating-point
    // target.
    Out.Normal = float4((normal + 1.0f) * 0.5f, 0.0f);
    Out.Depth  = In.NormalDepth.wwww;

    return Out;
}

#ifndef FX_COMPOSER

// Technique.
technique10 NormalDepth
{
    pass p0
    {
        SetVertexShader(CompileShader(vs_4_0, VS_NormalDepth()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_NormalDepth()));
    }
}

#endif
