//**************************************************************************/
// Copyright (c) 2010 Autodesk, Inc.
// All rights reserved.
// 
// These coded instructions, statements, and computer programs contain
// unpublished proprietary information written by Autodesk, Inc., and are
// protected by Federal copyright law. They may not be disclosed to third
// parties or copied or duplicated in any form, in whole or in part, without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/
// DESCRIPTION:  Spread the influence of motion vectors in the direction of motion.
// AUTHOR:  Kells Elmquist
// CREATED: November 2010
//**************************************************************************/

#include "Common10.fxh"    

/////////////////////////////////////////////////////////////////////////////
//
//	Spread motion vectors to affected pixels
//
// The  source velocity texure
uniform Texture2D	sourceVelocity;
uniform sampler		velocitySamp;

uniform int filterRadius = 16;   // in pixels, radius 4 = 9x9 samples; 8 = 17x17; side=2*radius+1
uniform float2 filterDirection;	// (0,1) for V pass or (1,0) for H pass
uniform int filterScale = 3;	// stride between pixel samples in motion spreading, 2x2 default

// Pixel shader.
// NOTE: This expects screen quad vertex shader output.
float4 spreadMotionBlur( VS_TO_PS_ScreenQuad In ) : SV_Target0
{
    // Compute the offset between samples in uv space
    float2 offset = (float)filterScale * filterDirection * gTexelSize;
	// get start uv
    float2 UV = In.UV - offset * filterRadius;
  
    float4 v0 = sourceVelocity.SampleLevel( velocitySamp, In.UV, 0 ); // center pix, for pass thru v0.zw
  
    // Get the velocoty value in each qualified sample point and average them
    float2 avgVelocity = (float2)0;
    float weightSum = 0.0f;
    for (int i = 0; i < (2*filterRadius+1); i++)
    {
		float4 vn = sourceVelocity.SampleLevel( velocitySamp, UV, 0 ); 
        float2 duv = (UV - In.UV);		// H or V vector from center to sample
        float duv2 = dot( duv, duv);	// square of length of duv
        float vn2 = 2.0f * dot( vn.xy, vn.xy); // square of length of vn
        
		// if the sample is a moving pixel this frame...
        if( (vn.w > 0 ||( dot((float2)1, abs(vn.xy)) > 0.001f ))
			&& (vn2 >= duv2)			    // affects in length
			&& (dot( vn.xy, duv) > -0.01f)    // non-opposite directions
		){
			avgVelocity += vn.xy;
			weightSum += 1.0f;
		}
		
        // Increment the texture coordinates by the offset.
        UV += offset;
	}
    if( weightSum != 0.0f )
		avgVelocity /= weightSum;
		
    return float4( avgVelocity.x, avgVelocity.y, v0.z, v0.w ); // preserve z & w from original
}

// shader for either pass of the 2 pass h/v spreading technique.
technique10 spreadMotionPass
{
    pass p0
    {
        SetVertexShader( CompileShader( vs_5_0, VS_ScreenQuad() ));
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_5_0, spreadMotionBlur() ));
    }
}
    

