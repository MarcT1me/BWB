#version 330 core

layout(location=0) in vec2 in_vert;

void main() {
    gl_Position = vec4(in_vert, 0.000001, 1.0);
}
