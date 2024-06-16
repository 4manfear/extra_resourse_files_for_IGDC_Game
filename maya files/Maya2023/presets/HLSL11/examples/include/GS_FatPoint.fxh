//**************************************************************************/
// Copyright (c) 2015 Autodesk, Inc.
// All rights reserved.
// 
// These coded instructions, statements, and computer programs contain
// unpublished proprietary information written by Autodesk, Inc., and are
// protected by Federal copyright law. They may not be disclosed to third
// parties or copied or duplicated in any form, in whole or in part, without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/

// Geometry shader that convert a point to a quad (2 triangles)
// You may need to define GS_FATPOINT_INPUT_STRUCT and GS_FATPOINT_INPUT_POSITION
// to match you own data

#ifndef GS_FATPOINT_INPUT_STRUCT
#define GS_FATPOINT_INPUT_STRUCT VS_TO_PS
#endif

#ifndef GS_FATPOINT_INPUT_POSITION
#define GS_FATPOINT_INPUT_POSITION HPos
#endif

float2 gsFatPointScreenSize : ViewportPixelSize <string UIWidget = "None"; >;
float2 gsFatPointSize <string UIWidget = "None"; > = {1, 1};

static const float4 cQuadPts[4] = {
	float4( -1.0,  1.0, 0, 0 ),
	float4( -1.0, -1.0, 0, 0 ),
	float4(  1.0,  1.0, 0, 0 ),
	float4(  1.0, -1.0, 0, 0 )};

[maxvertexcount(4)] 
void GS_FatPoint( point GS_FATPOINT_INPUT_STRUCT inputs[1] : SV_PATCH, inout TriangleStream<GS_FATPOINT_INPUT_STRUCT> outStream )
{
	GS_FATLINE_INPUT_STRUCT outS = inputs[0];

	float4 Pc = outS.GS_FATPOINT_INPUT_POSITION;

	float depthPriority = 0.001;
	Pc.z -= depthPriority;

	float size = max(0, max(gsFatPointSize.x, gsFatPointSize.y));
	float4 sizeInZ = float4(gsFatPointSize.xy / gsFatPointScreenSize.xy, 0, 0) * outS.GS_FATPOINT_INPUT_POSITION.w;
	for( int i = 0; i < 4; ++i ) {
		outS.GS_FATPOINT_INPUT_POSITION = Pc + sizeInZ * cQuadPts[i];
		outStream.Append( outS ); 
	}
	outStream.RestartStrip();
}

struct GS_FATPOINT_OUTPUT_STRUCT
{
	GS_FATPOINT_INPUT_STRUCT In;
	uint hwsPrimitiveID : SV_PrimitiveID;
};

[maxvertexcount(4)] 
void GS_FatPoint_ForHWSelection( point GS_FATPOINT_INPUT_STRUCT inputs[1] : SV_PATCH, uint hwsPrimitiveID : SV_PrimitiveID, inout TriangleStream<GS_FATPOINT_OUTPUT_STRUCT> outStream )
{
	GS_FATPOINT_OUTPUT_STRUCT outS;
	outS.In = inputs[0];
	outS.hwsPrimitiveID = hwsPrimitiveID;

	float4 Pc = outS.In.GS_FATPOINT_INPUT_POSITION;

	float depthPriority = 0.001;
	Pc.z -= depthPriority;

	float size = max(0, max(gsFatPointSize.x, gsFatPointSize.y));
	float4 sizeInZ = float4(gsFatPointSize.xy / gsFatPointScreenSize.xy, 0, 0) * outS.In.GS_FATPOINT_INPUT_POSITION.w;
	for( int i = 0; i < 4; ++i ) {
		outS.In.GS_FATPOINT_INPUT_POSITION = Pc + sizeInZ * cQuadPts[i];
		outStream.Append( outS ); 
	}
	outStream.RestartStrip();
}
