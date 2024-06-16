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
    float width : TEXCOORD0; 
    float3 curveVec : TEXCOORD1; 
    float offsetFlag : TEXCOORD2; 
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

//  Globals 
extern float4x4 World : world; 
extern float3 cameraDirection : viewdirection; 
extern float3 cameraPosition : worldcameraposition; 
extern bool camIsOrtho : isorthographic; 

float3 xgenVSWidthVec(float3 Pm, float width, float3 curveVec, float4x4 world, float3 viewDirection, float3 worldCameraPosition, bool camIsOrtho)
{
    float3 viewVec = viewDirection;
    if (!camIsOrtho) {
    float3 pw = mul(float4(Pm, 1.0f), world).xyz;
        viewVec = pw - worldCameraPosition;
    }

    return normalize(cross(viewVec, curveVec)) * width;
}

float3 xgenVSOffset(float3 Pm, float offsetFlag, float3 widthVecFinal)
{
    return Pm + offsetFlag * widthVecFinal;
}

float3 xgenVSNw(float3 widthVecFinal, float3 curveVec)
{
    return normalize(cross(widthVecFinal, curveVec));
}

// Vertex shader.
VS_TO_PS_NormalDepth VS_NormalDepth(VS_INPUT_NormalDepth In)
{
    VS_TO_PS_NormalDepth Out;

    float3 widthVecFinal = xgenVSWidthVec( In.Pos, In.width, In.curveVec, World, cameraDirection, cameraPosition, camIsOrtho ); 
    float4 pm4 = float4(xgenVSOffset( In.Pos, In.offsetFlag, widthVecFinal ), 1.0f); 
    float3 nw3 = xgenVSNw(widthVecFinal, In.curveVec);
    float3 nn = nw3;
    
    // Transform the vertex from object space to clip space.
    Out.HPos = mul(pm4, gWVPXf);
    
    // Record the normal and depth components for the pixel shader.
    // NOTE: This depends on whether the view direction is along +Z or -Z.  The projection matrix
    // "Z sense" determines this.
    Out.NormalDepth.xyz = mul(nn, gWVITXf);
    Out.NormalDepth.z = gProjZSense * Out.NormalDepth.z;
    Out.NormalDepth.w = gProjZSense * mul(pm4, gWVXf).z;

    #ifdef CLIPPING // D3D10 ONLY
        // Compute the eight clip distances.
        float4 HPw = mul(pm4, gWXf);
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
PS_OUT PS_NormalDepth(VS_TO_PS_NormalDepth In)
{
    PS_OUT Out;

    // Set the normal for an unsigned normalized integer target, and depth for a floating-point
    // target.
    Out.Normal = float4((normalize(In.NormalDepth.xyz) + 1.0f) * 0.5f, 0.0f);
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
