import moderngl
import pygame
from array import array
import glm


class ShaderProgram:
    def __init__(self, ctx: moderngl.Context, path, types, *attrs):
        self.path = path
        self.args = types, *attrs

        with open(rf'{path}.vert') as file:
            vert = file.read()

        with open(rf'{path}.frag') as file:
            frag = file.read()

        self.program = ctx.program(vert, frag)

    def set_uniform(self, key, value):
        try:
            self.program[key] = value
        except KeyError:
            print(f'not use uniform with name {key}')

    def release(self):
        self.program.release()


class SimpleModel:
    def __init__(self, ctx: moderngl.Context, shader: ShaderProgram):
        self.ctx = ctx

        self.shader = shader

        self.vbo = ctx.buffer(self.get_vertices())
        self.vao = ctx.vertex_array(self.shader.program, [(self.vbo, *self.shader.args)])

    def event(self, event):
        ...

    def update(self, dt, time):
        ...

    def render(self):
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)

    def get_vertices(self) -> array: ...

    def release(self):
        self.vbo.release()
        self.vao.release()


class Renderer:
    class Blit(SimpleModel):
        def use(self, surface, pos):
            # creating texture
            texture = self.ctx.texture(surface.get_size(), 4, data=pygame.image.tostring(surface, 'RGBA'))
            # texture blit methods
            texture.use(0)  # use current texture
            self.shader.program['textureRect'] = (*pos, *glm.ivec2(surface.get_size())/2)  # change blit program params
            self.vao.render(mode=moderngl.TRIANGLE_STRIP)  # render vao himself
            texture.release()

        def get_vertices(self) -> array:
            return array('f', [
                # position (x, y), uv cords (x, y)
                -1.0, -1.0, 0.0, 1.0,  # bottom left
                1.0, -1.0, 1.0, 1.0,  # bottom right
                -1.0, 1.0, 0.0, 0.0,  # top left
                1.0, 1.0, 1.0, 0.0,  # top right
            ])

    def __init__(self, res: tuple[int, int]):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.res = glm.vec2(res)

        self.win = pygame.display.set_mode(res, pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND | moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self.programs = {
            'blit': ShaderProgram(self.ctx, 'shaders\\blit', '2f 2f', 'aPos', 'aTexCoord'),
        }
        self.programs['blit'].set_uniform('screenResolution', res)

        self._blit_instance = Renderer.Blit(self.ctx, self.programs['blit'])
        self.blit = lambda surface, pos: self._blit_instance.use(surface, pos)

    def __enter__(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1.0))

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.display.flip()
        return False

    def release(self):
        self._blit_instance.release()
        [program.release() for program in self.programs.values()]
        self.ctx.release()


class Scene:
    def __init__(self, renderer: Renderer, objects=dict()):
        self.renderer = renderer
        self.objects = objects

    def event(self, event):
        [o.event(event) for o in self.objects.values()]

    def update(self, dt, time):
        [o.update(dt, time) for o in self.objects.values()]

    def render(self):
        [o.render() for o in self.objects.values()]

    def release(self):
        [o.release() for o in self.objects.values()]


class App:
    def __init__(self, res, fps):
        self.running = True
        self.scene: Scene = ...
        self.renderer = Renderer(res)
        self.fps = fps
        self.dt = 0
        self.time = 0
        self.clock = pygame.time.Clock()

    def event(self, event):
        ...

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.event(event)

    def update(self):
        ...

    def render(self):
        ...

    def run(self):
        while self.running:
            self.events()
            self.time = pygame.time.get_ticks() / 1000
            self.update()
            self.render()
            self.dt = self.clock.tick(self.fps)
        self.on_exit()

    def on_exit(self):
        pygame.quit()
        self.scene.release()
        self.renderer.release()
