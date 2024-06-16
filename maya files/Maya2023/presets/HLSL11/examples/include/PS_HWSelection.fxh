//**************************************************************************/
// Copyright (c) 2015,2018 Autodesk, Inc.
// All rights reserved.
// 
// These coded instructions, statements, and computer programs contain
// unpublished proprietary information written by Autodesk, Inc., and are
// protected by Federal copyright law. They may not be disclosed to third
// parties or copied or duplicated in any form, in whole or in part, without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/

// Simple pixel shader that performs hardware selection :
// return the object/component id as the pixel color
// You may need to define PS_HWSELECTION_INPUT_STRUCT
// to match you own data

#ifndef PS_HWSELECTION_INPUT_STRUCT
#define PS_HWSELECTION_INPUT_STRUCT VS_TO_PS
#endif

bool gsHWSIsObjectLevel : HWS_ObjectLevel <string UIWidget = "None"; > = false;
int gsHWSPrimitiveBase : HWS_PrimitiveBase <string UIWidget = "None"; > = 0;

// Pixel shader used for Viewport 2.0 hardware selection
float4 PS_HWSelection(PS_HWSELECTION_INPUT_STRUCT In, uint hwsPrimitiveID : SV_PrimitiveID ) : SV_Target
{
	int colorID = gsHWSPrimitiveBase;
	if (!gsHWSIsObjectLevel)
		colorID += hwsPrimitiveID;

	float4 color;
	color.x = float(colorID & 0x000000FF) / 255.0;
	color.y = float((colorID & 0x0000FF00) >> 8) / 255.0;
	color.z = float((colorID & 0x00FF0000) >> 16) / 255.0;
	color.w = float((colorID & 0xFF000000) >> 24) / 255.0;
	return color;
}
