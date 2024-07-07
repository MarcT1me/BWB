#version 330 core

// shader args
layout (location = 0) in vec2 aPos; // Vertex position attribute
layout (location = 1) in vec2 aTexCoord; // Texture coordinate attribute
// blit params
uniform ivec2 screenResolution; // Screen resolution uniform
uniform ivec4 textureRect; // Texture rect uniform (x, y, width, height)
// fragment params
out vec2 TexCoords; // Output texture coordinate


void main() {
    // Calculate the vertex position based on the texture rect, screen resolution, and alignment
    vec2 vertexPos = vec2(
        (                     textureRect.x + textureRect.z + aPos.x * textureRect.z) / screenResolution.x * 2.0 - 1,
        (screenResolution.y - textureRect.y - textureRect.w + aPos.y * textureRect.w) / screenResolution.y * 2.0 - 1
    );
    gl_Position = vec4(vertexPos, 0.0, 1.0); // Set the final vertex position

    // Pass the texture coordinate
    TexCoords = aTexCoord;
}