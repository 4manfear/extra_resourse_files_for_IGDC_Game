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

// Simple pixel shader that renders as geometry with a solid color
// You may need to define PS_SOLIDCOLOR_INPUT_STRUCT
// to match you own data

#ifndef PS_SOLIDCOLOR_INPUT_STRUCT
#define PS_SOLIDCOLOR_INPUT_STRUCT VS_TO_PS
#endif

float4 gsSolidColor <string UIWidget = "None"; > = {0, 0, 0, 1};

float4 PS_SolidColor(PS_SOLIDCOLOR_INPUT_STRUCT In) : SV_Target
{
	return gsSolidColor;	
}
