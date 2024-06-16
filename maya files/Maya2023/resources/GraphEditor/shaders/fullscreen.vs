#version 330 core

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec2 inTex;
    
out VS_OUT
{
    vec2 tex;
}vs_output;

void main()
{  
    gl_Position    = vec4( inPos, 0.0f, 1.0f );
    vs_output.tex  = inTex;
}