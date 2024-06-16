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

// Geometry shader that convert a line to a rectangle (2 triangles)
// You may need to define GS_FATLINE_INPUT_STRUCT and GS_FATLINE_INPUT_POSITION
// to match you own data

#ifndef GS_FATLINE_INPUT_STRUCT
#define GS_FATLINE_INPUT_STRUCT VS_TO_PS
#endif

#ifndef GS_FATLINE_INPUT_POSITION
#define GS_FATLINE_INPUT_POSITION HPos
#endif

float2 gsFatLineScreenSize : ViewportPixelSize <string UIWidget = "None"; >;
float2 gsFatLineWidth <string UIWidget = "None"; > = {1, 1};

[maxvertexcount(4)] 
void GS_FatLine( line GS_FATLINE_INPUT_STRUCT inputs[2] : SV_PATCH, inout TriangleStream<GS_FATLINE_INPUT_STRUCT> outStream )
{
	GS_FATLINE_INPUT_STRUCT out0 = inputs[0];
	GS_FATLINE_INPUT_STRUCT out1 = inputs[1];

	float4 Pc0 = out0.GS_FATLINE_INPUT_POSITION;
	float4 Pc1 = out1.GS_FATLINE_INPUT_POSITION;

	float depthPriority = 0.001;
	Pc0.z -= depthPriority;
	Pc1.z -= depthPriority;

	float3 aline = Pc0.xyz / Pc0.w - Pc1.xyz / Pc1.w;
	float len = length(aline);
	aline /= len;
	float3 norm = float3(0,0,1.0);
	float3 ortho = cross(normalize(aline - dot(aline, norm) * norm), norm);
	float extlen = gsFatLineWidth.x / sqrt(aline.x*aline.x*gsFatLineScreenSize.x*gsFatLineScreenSize.x + aline.y*aline.y*gsFatLineScreenSize.y*gsFatLineScreenSize.y);
	float lambda = extlen / len;
	float lambdaN = -lambda;
	float lambdaC = (Pc0.w * lambdaN) / ((Pc0.w * lambdaN) + Pc1.w * (1 - lambdaN));
	lambdaC = lambdaC > 0 ? -1.0e3f : lambdaC;
	float4 ext0 = (1 - lambdaC) * Pc0 + lambdaC * Pc1;
	out0.GS_FATLINE_INPUT_POSITION = ext0;
	float3 scale = float3(1, 1, 1);
	scale.xy = float2((out0.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.x, (out0.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.y);
	ortho *= gsFatLineWidth.y;
	out0.GS_FATLINE_INPUT_POSITION.xyz += ortho * scale;
	outStream.Append( out0 ); 
	out0.GS_FATLINE_INPUT_POSITION.xyz -= (ortho * 2) * scale;
	outStream.Append( out0 ); 

	lambdaN = 1 + lambda;
	lambdaC = (Pc0.w * lambdaN) / ((Pc0.w * lambdaN) + Pc1.w * (1 - lambdaN));
	lambdaC = lambdaC < 0 ? 1.0e3f : lambdaC;
	float4 ext1 = (1 - lambdaC) * Pc0 + lambdaC * Pc1; out1.GS_FATLINE_INPUT_POSITION = ext1;
	scale.xy = float2((out1.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.x, (out1.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.y);
	out1.GS_FATLINE_INPUT_POSITION.xyz += ortho * scale;
	outStream.Append( out1 ); 
	out1.GS_FATLINE_INPUT_POSITION.xyz -= (ortho * 2) * scale;
	outStream.Append( out1 ); 
	outStream.RestartStrip(); 
}

struct GS_FATLINE_OUTPUT_STRUCT
{
	GS_FATLINE_INPUT_STRUCT In;
	uint hwsPrimitiveID : SV_PrimitiveID;
};

[maxvertexcount(4)] 
void GS_FatLine_ForHWSelection( line GS_FATLINE_INPUT_STRUCT inputs[2] : SV_PATCH, uint hwsPrimitiveID : SV_PrimitiveID, inout TriangleStream<GS_FATLINE_OUTPUT_STRUCT> outStream )
{
	GS_FATLINE_OUTPUT_STRUCT out0, out1;
	out0.In = inputs[0];
	out0.hwsPrimitiveID = hwsPrimitiveID;
	out1.In = inputs[1];
	out1.hwsPrimitiveID = hwsPrimitiveID;

	float4 Pc0 = out0.In.GS_FATLINE_INPUT_POSITION;
	float4 Pc1 = out1.In.GS_FATLINE_INPUT_POSITION;

	float depthPriority = 0.001;
	Pc0.z -= depthPriority;
	Pc1.z -= depthPriority;

	float3 aline = Pc0.xyz / Pc0.w - Pc1.xyz / Pc1.w;
	float len = length(aline);
	aline /= len;
	float3 norm = float3(0,0,1.0);
	float3 ortho = cross(normalize(aline - dot(aline, norm) * norm), norm);
	float extlen = gsFatLineWidth.x / sqrt(aline.x*aline.x*gsFatLineScreenSize.x*gsFatLineScreenSize.x + aline.y*aline.y*gsFatLineScreenSize.y*gsFatLineScreenSize.y);
	float lambda = extlen / len;
	float lambdaN = -lambda;
	float lambdaC = (Pc0.w * lambdaN) / ((Pc0.w * lambdaN) + Pc1.w * (1 - lambdaN));
	lambdaC = lambdaC > 0 ? -1.0e3f : lambdaC;
	float4 ext0 = (1 - lambdaC) * Pc0 + lambdaC * Pc1;
	out0.In.GS_FATLINE_INPUT_POSITION = ext0;
	float3 scale = float3(1, 1, 1);
	scale.xy = float2((out0.In.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.x, (out0.In.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.y);
	ortho *= gsFatLineWidth.y;
	out0.In.GS_FATLINE_INPUT_POSITION.xyz += ortho * scale;
	outStream.Append( out0 ); 
	out0.In.GS_FATLINE_INPUT_POSITION.xyz -= (ortho * 2) * scale;
	outStream.Append( out0 ); 

	lambdaN = 1 + lambda;
	lambdaC = (Pc0.w * lambdaN) / ((Pc0.w * lambdaN) + Pc1.w * (1 - lambdaN));
	lambdaC = lambdaC < 0 ? 1.0e3f : lambdaC;
	float4 ext1 = (1 - lambdaC) * Pc0 + lambdaC * Pc1; out1.In.GS_FATLINE_INPUT_POSITION = ext1;
	scale.xy = float2((out1.In.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.x, (out1.In.GS_FATLINE_INPUT_POSITION.w) / gsFatLineScreenSize.y);
	out1.In.GS_FATLINE_INPUT_POSITION.xyz += ortho * scale;
	outStream.Append( out1 ); 
	out1.In.GS_FATLINE_INPUT_POSITION.xyz -= (ortho * 2) * scale;
	outStream.Append( out1 ); 
	outStream.RestartStrip(); 
}
