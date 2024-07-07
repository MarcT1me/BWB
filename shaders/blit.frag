#version 330 core

// final color
layout(location=0) out vec4 f_color;
// texture
in vec2 TexCoords;
uniform sampler2D u_texture_0;

void main() {
    // blit texture on rect
    f_color = texture(u_texture_0, TexCoords);
}