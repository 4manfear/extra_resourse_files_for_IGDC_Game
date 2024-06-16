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
// DESCRIPTION: Screen space ambient occlusion - random sphere samples (D3D10).
// AUTHOR: Mauricio Vives
// CREATED: October 2008
//**************************************************************************/

#ifndef _SSAO_SAMPLES_FXH_
#define _SSAO_SAMPLES_FXH_

// The large array data struct is slower than texture accessing, especially OpenGL core profile. 
// Normally, DX11 & OpenGL array accessing has the same performance with texture accessing.
// We can define the macro "USE_ARRAY_LOOK_UP" to try it out.
// By default we get the random sphere samples from texture sampling.
#if USE_ARRAY_LOOKUP

// The array of sampling offsets, which are random vectors inside the unit sphere.
static float3 gOffsets[64] = 
{
    {0.0792077, 0.0144504, 0.0277842},
    {0.097627, 0.185689, 0.430379},
    {0.089766, 0.694503, -0.152690},
    {0.247127, 0.291788, -0.231237},
    {-0.124826, -0.404931, 0.783546},
    {0.363641, -0.100100, -0.280984},
    {0.226127, -0.125936, 0.804697},
    {0.152315, -0.207803, 0.184084},
    {0.360111, -0.105749, -0.101605},
    {0.627596, -0.176360, -0.206989},
    {0.287980, -0.210261, -0.152290},
    {0.432149, 0.320347, -0.424018},
    {0.181746, 0.103633, 0.148651},
    {-0.264876, -0.805480, -0.128270},
    {-0.253419, -0.092915, -0.159849},
    {0.459981, 0.499998, -0.656741},
    {-0.321192, 0.042073, -0.020902},
    {0.587395, -0.073098, -0.552151},
    {-0.376110, 0.108485, -0.203558},
    {-0.575219, -0.580312, -0.555114},
    {-0.092606, 0.354163, 0.073158},
    {0.214090, 0.793343, 0.429394},
    {0.291569, 0.176634, -0.350634},
    {0.662097, 0.039422, 0.257964},
    {0.408949, -0.207881, -0.073700},
    {0.130843, 0.680857, -0.633440},
    {0.024787, -0.028745, 0.160894},
    {0.212951, -0.323682, -0.563194},
    {-0.027681, 0.260896, 0.417096},
    {0.748576, -0.003720, -0.413959},
    {-0.281457, -0.333710, -0.201002},
    {-0.837797, -0.396338, -0.185518},
    {-0.047046, -0.396803, -0.024131},
    {0.391251, 0.705270, -0.432962},
    {-0.083722, 0.006855, 0.181968},
    {0.243357, 0.151502, 0.726045},
    {-0.289262, -0.112243, -0.286586},
    {-0.216451, -0.967343, 0.063698},
    {-0.151822, -0.004644, 0.109376},
    {-0.144331, -0.425897, 0.645119},
    {0.476781, 0.004779, 0.110723},
    {0.097038, 0.734579, 0.039286},
    {0.361029, 0.060178, 0.244769},
    {-0.590153, 0.354229, -0.316604},
    {0.278055, 0.352485, 0.096723},
    {0.758470, -0.454634, 0.087356},
    {0.370184, 0.019614, 0.297197},
    {-0.115929, 0.982283, 0.039905},
    {0.430416, 0.057880, 0.046013},
    {-0.650683, 0.327732, -0.344024},
    {-0.381497, -0.044707, -0.193564},
    {-0.432000, 0.266124, -0.523173},
    {0.184161, -0.325045, -0.136430},
    {-0.290988, -0.806392, 0.314040},
    {-0.313217, 0.304618, 0.182054},
    {0.643437, 0.318353, -0.194466},
    {-0.457773, -0.058758, -0.053620},
    {-0.768332, -0.040492, -0.085882},
    {0.278374, -0.237206, -0.201678},
    {-0.956053, -0.136480, -0.250495},
    {0.425854, -0.134032, -0.146113},
    {0.056468, -0.396615, -0.301119},
    {-0.270911, -0.088203, 0.002126},
    {0.284703, -0.247222, -0.491950}
};

float3 GetOffset(int id)
{
	return gOffsets[id].xyz;
}

// Use texture lookup
#else

// SSAO sample texture is a 64x1 texture. It stores 64 offsets values in B8G8R8 unorm.
Texture2D gSSAOSampleTex
<
    string UIName = "SSAO Sample Texture";
    string ResourceName = "SSAOSample.bmp";
> = NULL;

float3 GetOffset(int id)
{
	float3 raw = gSSAOSampleTex.Load(int3(id,0,0));
	return raw*2.0 - 1.0;
}

#endif

#endif // _SSAO_SAMPLES_FXH_