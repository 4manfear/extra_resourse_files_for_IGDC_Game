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
// DESCRIPTION:  Spread the influence of DOF to neighboring pixels.
// AUTHOR:  Kells Elmquist
// CREATED: November 2010
//**************************************************************************/

#include "Common10.fxh"    

/////////////////////////////////////////////////////////////////////////////
//
//	Spread DOF circles of confusion to affected pixels
//
// The  source image texure to be blurred
uniform Texture2D source;
uniform sampler sourceSamp;

// the coc/depth texture is a float2 texture that has no-abs coc in .x & linear depth in .y
uniform Texture2D cocDepth;
uniform sampler cocDepthSamp;

#ifdef USE_NONPE_MASK
// 0 if the pixel is affected by post effects and 1 is otherwise
uniform Texture2D postFXMask;
uniform sampler postFXMaskSamp;
#endif

uniform int		searchRadius1 = 1;	    // in pixels, radius 1 = 3x3 samples; side=2*radius+1
uniform int		sampleSpacing1 = 1;		// stride between pixel samples in search, 1x1 default
uniform int		searchRadius2 = 3;		// in pixels, radius 3 = 7x7 samples
uniform int		sampleSpacing2 = 2;		// stride between pixel samples in motion spreading, 1x1 default
uniform float	acceptThreshold = 0.05f;// similarity threshold to accept neighbor coc
uniform float	cocAtInfinity = 0.1f;	// aka alpha, its in uv coords 
uniform float	spreadScale = 1.0f;		// spacing of 3x3, each sample represents an area of 9 pixels 
uniform float   maxCocScale = 2.0f;		// hack factor for maxCoc, correct value is too small

// filter kernel, return value of kernel of radius r at a distance x from the filter center
// both x & r must be positive, r must be > 0
float filter( float r, float x )
{
	//return 1.0f;
	// test for sharp
	if( r < 0.00001f ) return 1;
	// linear (triangle) kernel
	return saturate( 1.0f - x/r );
	// gaussian kernel
	//return 0.79788f * exp( -x*x/(0.375 * r*r) ) / r;
}

// DOF Pixel shader. multi pass variable scale search & reverse filter, 
// NOTE: This expects the common screen quad vertex shader output in common.cgh.
float4 spreadDOFBlur( VS_TO_PS_ScreenQuad In ) : SV_Target0
{
    // Compute the offset between samples in uv space, spacing always 1 for first pass
    float2 offset = (float)sampleSpacing1 * gTexelSize;
	int count = 2 * searchRadius1 + 1; // search count x count samples

	float maxCoc = maxCocScale 
		* max(offset.x, offset.y) 
		* ( max((float)searchRadius1, (float)searchRadius2) + 0.5f);
    
	// center pixel
    float4 c0 = cocDepth.SampleLevel( cocDepthSamp, In.UV, 0 ); 

	// fixup the coc for bgnd pixels, buffer is cleared to 10e6
	if( c0.y > 999990 )
		c0.x = cocAtInfinity;
	float coc0 = min( abs( c0.x ), maxCoc );
	float wSum = filter( coc0, 0.0f );

	// color sums: infront, center, both work as rgba and have local sum of weights in frontW and centerW respectively
    float4 centerSum = wSum * source.SampleLevel( sourceSamp, In.UV, 0 ); 
	float4 infrontSum = (float4)0;
	float centerW = 1.0;
	float frontW = 0.0;

	// get start uv, clr & weight sums
    float2 UV = In.UV - offset * (float)searchRadius1;
	float u0 = UV.x;

    // collect each qualified sample point, then weight & average them
	// for each row
    for (int i = 0; i < count; i++)
	{
		// for each pixel in the row
		for (int j = 0; j < count; j++)
		{
			if( i==searchRadius1 && j==searchRadius1 ) // no center
				continue;

			float4 cn = cocDepth.SampleLevel( cocDepthSamp, UV, 0 );

			// fixup the coc for bgnd pixels, buffer is cleared to 10e6
			if( cn.y > 999990 )
				cn.x = cocAtInfinity;

			float coc = min( abs( cn.x ), maxCoc );

			// d is the distance from center to sample in uv space
			float d = length( UV - In.UV );

#ifdef USE_NONPE_MASK
			bool includePostEffects = postFXMask.SampleLevel( postFXMaskSamp, UV, 0 ).a == 0.0f;
#else
			// The z component is 0.0 by default. If it is 1.0, the pixel
			// will need to be excluded from post effects.
			bool includePostEffects = (cn.z < 0.5f);
#endif

			// qualify samples by z, note z is stored in y field of float2
			// & see if coc of sample overlaps center pixel, coc >= d, 
			if( coc >= d && includePostEffects )
			{
				// get the scene sample at UV
				float4 sn = source.SampleLevel( sourceSamp, UV, 0 ); 
				float w = filter( coc, d );
				wSum += w;
				// & classify sample by coc ...
		 	    //if( abs(coc - coc0) <= acceptThreshold )		// coc band method
				float dInPix = d / gTexelSize.x;				// texelSz in 1/width, so d in pixels is d * width.
		 	    if( abs(coc - coc0)/dInPix <= acceptThreshold )	// coc max gradient method	
				{ // within near coc threshold band
					centerSum += w * sn;
					centerW += w;
				}
				else if( coc < coc0 )
				{ // sample is in front of c0
					infrontSum += w * sn;
					frontW += w;
				}
			}

			// Increment the texture coordinates by the offset in x, next pixel in row
			UV.x += offset.x;
		} // for each j

		// Increment the texture coordinates by the offset in y, next row
		UV.x = u0;
		UV.y += offset.y;
	} // for each i

	// optional second, scaled search area
	// second pass, use the given sample spacing
    offset = (float)sampleSpacing2 * gTexelSize;
	count = 2 * searchRadius2 + 1; // search count x count samples

    UV = In.UV - offset * searchRadius2;
	u0 = UV.x;
    // collect each qualified sample point
    for (int ii = 0; ii < count; ii++)
	{
		for (int jj = 0; jj < count; jj++)
		{
			if( ii==searchRadius2 && jj==searchRadius2 ) continue;

			float4 cn = cocDepth.SampleLevel( cocDepthSamp, UV, 0 ); //use sampleLevel 0 to avoid implicit derivs

			if( cn.y > 999990.0f ) cn.x = cocAtInfinity;

			float coc = min( abs( cn.x ), maxCoc );
			float d = length( UV - In.UV );	

#ifdef USE_NONPE_MASK
			bool includePostEffects = postFXMask.SampleLevel( postFXMaskSamp, UV, 0 ).a == 0.0f;
#else
			// The z component is 0.0 by default. If it is 1.0, the pixel
			// will need to be excluded from post effects.
			bool includePostEffects = (cn.z < 0.5f);
#endif

			if( coc >= d && includePostEffects )
			{
				float4 sn = source.SampleLevel( sourceSamp, UV, 0 ); 

				float w = spreadScale * filter( coc, d );
				wSum += w;
				// & classify sample by coc ...
		 	    //if( abs(coc - coc0) <= acceptThreshold )		// coc band method
				float dInPix = d / gTexelSize.x; // texelSz in 1/width, so d in pixels is d * width.
		 	    if( abs(coc - coc0)/dInPix <= acceptThreshold )	// coc max gradient method	
				{
					centerSum += w * sn;
					centerW += w;
				}
				else if( coc < coc0 )
				{
					infrontSum += w * sn;
					frontW += w;
				}
			}
			UV.x += offset.x;
		} 
		UV.x = u0;
		UV.y += offset.y;
	} // for each i

	// normalize front & center sums separately
	// always true, initialized : if( centerW != 0.0f ) 
	centerSum /= centerW;
	if( frontW != 0.0f ) infrontSum /= frontW;

	// blend the front over the center. scale by 2
	float frontBlend = saturate( frontW / wSum );
    return lerp( centerSum, infrontSum, frontBlend );
}

// shader for either pass of the 2 pass h/v spreading technique.
technique10 spreadDOFPass
{
    pass p0
    {
        SetVertexShader( CompileShader( vs_5_0, VS_ScreenQuad() ));
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_5_0, spreadDOFBlur() ));
    }
}
    