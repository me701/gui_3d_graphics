#version 120

attribute highp vec4 vertex;    // location,
uniform highp mat4 matrix;      // transformation,
attribute lowp vec4 color_attr; // and color (all from PyQt app)
varying lowp vec4 color;        // color for fragments (from OpenGL)

void main(void)
{
    gl_Position = matrix * vertex; // vertex = 4-element vector.
    color = color_attr;             // see, matrix-vector is important!
}