#version 330 core

const float kDoubleEpsilon = 1e-6;

layout(std140) uniform PerFrame
{
    layout(column_major) mat4 projection;                               // transform world space into NDC space [-1,1].
    layout(column_major) mat4 projectionWithoutHorizontalTranslation;   
    layout(column_major) mat4 viewportInv;                              // transform viewport space(pixel) into NDC space [-1,1].
    layout(column_major) mat4 viewport;                                 // transform NDC [-1,1] into viewport space(pixel).
    int   projectionOffsetXSec;
    int   projectionOffsetXFrac;
    uint displayPoint;
    float viewRegionMinX;
    float viewRegionMaxX;
    float viewRegionMinY;
    float viewRegionMaxY;  
    float viewRegionWidth;
    float keysDensity;
} perFrame;

layout(std140) uniform CustomLineSettings
{
    uint stipple;
	float lineWidth;
} customLineSettings;

layout(lines) in;
layout(line_strip, max_vertices=2) out;

in VS_OUT
{
    vec4 color;
} gs_input[];

out GS_OUT
{
    vec4  color;
    float stippleLineCoord;
	flat uint pattern;
} gs_output;

void main()
{
	// For line stippling, map the two end points to screen space, and find the
	// intersection of the line through the two points with either the x=0
	// axis, or the y=0 axis, depending on the slope of the line.  Calculate
	// the distance from both points to the axis point, taking into account
	// the side of the axis on which they lie.
	//
    vec2 lPt0InPixel = (perFrame.viewport * gl_in[0].gl_Position).xy;
    vec2 lPt1InPixel = (perFrame.viewport * gl_in[1].gl_Position).xy;
	vec2 axisPoint;
    
	float x0 = lPt0InPixel.x;
	float y0 = lPt0InPixel.y;
	float x1 = lPt1InPixel.x;
	float y1 = lPt1InPixel.y;

	float dx = x1 - x0;
	float dy = y1 - y0;

	float adx = dx;
	if( adx < 0.0f ){
		adx = -adx;
	}
	float ady = dy;
	if( ady < 0.0f ){
		ady = -ady;
	}
	float d1 = 0.0f;
	float d0 = 0.0f;
	// Line equation: L(t) = (x0,y0) + t(dx,dy)
	//
	if( ( adx > ady ) && (adx > kDoubleEpsilon) ){
		// Find intersection with y=0
		//
		axisPoint.x = 0.0f;
		axisPoint.y = y0 - (x0*dy)/dx;
		d1 = length( lPt1InPixel - axisPoint );
		d0 = length( lPt0InPixel - axisPoint );
		if( x0 < 0.0f ){
			d0 = -d0;
		}
		if( x1 < 0.0f ){
			d1 = -d1;
		}
	} else if( ady > kDoubleEpsilon ){
		// Find intersection with x=0
		//
		axisPoint.x = x0 - (y0*dx)/dy;
		axisPoint.y = 0.0f;
		d1 = length( lPt1InPixel - axisPoint );
		d0 = length( lPt0InPixel - axisPoint );
		if( y0 < 0.0f ){
			d0 = -d0;
		}
		if( y1 < 0.0f ){
			d1 = -d1;
		}
	}

    gl_Position = gl_in[0].gl_Position;
    gs_output.color = gs_input[0].color;
    gs_output.stippleLineCoord = d0;
	gs_output.pattern = customLineSettings.stipple;
    EmitVertex();

    gl_Position = gl_in[1].gl_Position;
    gs_output.color = gs_input[1].color;
    gs_output.stippleLineCoord = d1;
	gs_output.pattern = customLineSettings.stipple;
    EmitVertex();
}
