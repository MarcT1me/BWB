from program import *
from random import random
import glm
import pygame


class Ball:
    def __init__(self, pos, vel, color, radius):
        self.pos = glm.vec2(pos)
        self.vel = glm.vec2(vel)
        self.color = color
        self.radius = radius
    
    def update(self, dt):
        self.vel = glm.normalize(self.vel)
        self.pos += glm.vec2(self.vel)*dt*0.1


class BallList(SimpleModel):
    def __init__(self, ctx, program):
        super().__init__(ctx, program)
        self._list_size = 341
        self.ball_list: list[Ball] = []
    
    def set_u_ball(self, index, name, value):
        self.shader.program[f'balls[{index}].{name}'].value = value
    
    def add(self, pos, vel, color, radius):
        next_index = len(self.ball_list)
        if next_index < self._list_size:
            ball = Ball(pos, vel, color, radius)
            self.ball_list.append(ball)
            self.set_u_ball(next_index, 'pos', ball.pos)
            self.set_u_ball(next_index, 'color', ball.color)
            self.set_u_ball(next_index, 'radius', ball.radius)
            self.shader.program['ballCounted'].value = next_index + 1
    
    def get_vertices(self) -> array:
        return array(
            'f', [
                # position (x, y)
                -1, -1.0,  # bottom left
                1, -1.0,  # bottom right
                -1, 1.0,  # top left
                1, 1.0,  # top right
            ]
        )
    
    def update(self, dt, time):
        for L in range(len(self.ball_list)):
            cur_ball = self.ball_list[L]
            for R in range(L + 1, len(self.ball_list)):
                cur_twin = self.ball_list[R]
                line = cur_ball.pos - cur_twin.pos
                if glm.length(line) <= cur_ball.radius + cur_twin.radius:
                    cur_ball.vel += glm.normalize(line)
                    cur_ball.vel -= glm.normalize(line)
                    
                    cur_twin.vel -= glm.normalize(line)
                    cur_ball.vel += glm.normalize(line)
                
            # border rebound
            win_size = pygame.display.get_window_size()
            if cur_ball.pos.x + cur_ball.radius > win_size[0] and cur_ball.vel.x > 0:
                cur_ball.vel.x *= -1
            if cur_ball.pos.y + cur_ball.radius > win_size[1] and cur_ball.vel.y > 0:
                cur_ball.vel.y *= -1
            if cur_ball.pos.x - cur_ball.radius < 0 and cur_ball.vel.x < 0:
                cur_ball.vel.x *= -1
            if cur_ball.pos.y - cur_ball.radius < 0 and cur_ball.vel.y < 0:
                cur_ball.vel.y *= -1
        
        for i in range(len(self.ball_list)):
            cur_ball = self.ball_list[i]
            cur_ball.update(dt)
            self.set_u_ball(i, 'pos', cur_ball.pos)


class BallFrame(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer.programs['ball'] = ShaderProgram(
            self.renderer.ctx, 'shaders\\balls',
            '2f', 'in_vert'
        )
        self.ball_list = BallList(self.renderer.ctx, self.renderer.programs['ball'])
        self.objects['ball_list'] = self.ball_list
        
        for i in range(10):
            self.add_random_ball((self.renderer.res.x*random(), self.renderer.res.y*random()))
    
    def add_random_ball(self, pos):
        angle = glm.radians(360*random())
        self.ball_list.add(
            pos=pos, vel=(glm.cos(angle), glm.sin(angle)),
            color=glm.vec3(random(), random(), random()), radius=10
        )
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.add_random_ball((100, 100))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_pos = pygame.mouse.get_pos()
                self.add_random_ball((m_pos[0], self.renderer.res.y - m_pos[1]))
        self.ball_list.event(event)
    
    def update(self, dt, time):
        self.ball_list.update(dt, time)
