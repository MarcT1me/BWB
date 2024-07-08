#version 330 core

layout(location=0) out vec4 f_color;

#define BALL_LIST_SIZE 341

struct Ball {
    vec2 pos;
    vec3 color;
    int radius;
};
uniform int ballCounted = 0;
uniform Ball balls[BALL_LIST_SIZE];


void main() {
    vec3 color;
    for (int i = 0; i < ballCounted; i++) {
        Ball ball = balls[i];
        if (length(gl_FragCoord.xy - ball.pos) <= ball.radius) {
            color += ball.color;
        }
    }
    f_color = vec4(color, 1);
}
