#version 330 core


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
}perFrame;

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec4 inColor;

out VS_OUT
{
	vec4 color;
} vs_output;

void main()
{

	gl_Position      = perFrame.projection * vec4( inPos, 0.0f, 1.0f );
	vs_output.color  = inColor;
}
