#version 330 core

layout(std140) uniform PerFrame
{
    layout(column_major) mat4 projection;                               // transform world space into NDC space [-1,1].
    layout(column_major) mat4 projectionWithoutHorizontalTranslation;   
    layout(column_major) mat4 viewportInv;                              // transform viewport space(pixel) into NDC space [-1,1].
    layout(column_major) mat4 viewport;                                 // transform NDC [-1,1] into viewport space(pixel).
    int   projectionOffsetX;
    uint displayPoint;
    float viewRegionMinX;
    float viewRegionMaxX;
    float viewRegionMinY;
    float viewRegionMaxY;  
    float viewRegionWidth;
    float keysDensity;
} perFrame;

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
} gs_output;

void main()
{
    vec4 lPt1InPixel = perFrame.viewport * gl_in[0].gl_Position;
    vec4 lPt2InPixel = perFrame.viewport * gl_in[1].gl_Position;
    
    gl_Position = gl_in[0].gl_Position;
    gs_output.color = gs_input[0].color;
    gs_output.stippleLineCoord = length( lPt1InPixel - lPt2InPixel );
    EmitVertex();

    gl_Position = gl_in[1].gl_Position;
    gs_output.color = gs_input[1].color;
    gs_output.stippleLineCoord = 0.0f;
    EmitVertex();
}
