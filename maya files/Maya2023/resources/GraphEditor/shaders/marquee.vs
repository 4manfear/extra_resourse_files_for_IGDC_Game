#version 330 core

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec4 inColor;

out VS_OUT
{
	vec4 color;
} vs_output;

void main()
{
	gl_Position      = vec4( inPos, 0.0f, 1.0f );
	vs_output.color  = inColor;
}
