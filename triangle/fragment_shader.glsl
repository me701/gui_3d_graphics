// The fragment shader is responsible for coloring
// the fragment.

#version 120

varying lowp vec4 color;

void main(void)
{
    gl_FragColor = color;
}