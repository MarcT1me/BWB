from balls import *
import pygame


class BallGame(App):
    def __init__(self):
        super().__init__((720, 480), 0)
        self.scene = BallFrame(self.renderer)

        self.fps_font = pygame.font.SysFont('Arial', 30)
        self.count_font = pygame.font.SysFont('Arial', 30)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        self.scene.event(event)

    def update(self):
        self.scene.update(self.dt, self.time)

    def render(self):
        fin_fps_font = self.fps_font.render(f'fps: {round(self.clock.get_fps())}', True, 'cyan')
        fin_cuont_font = self.count_font.render(f'balls counted: {len(self.scene.ball_list.ball_list)}', True, 'cyan')
        with self.renderer:
            self.scene.render()
            self.renderer.blit(
                fin_cuont_font,
                (0, int(self.renderer.res.y - fin_cuont_font.get_height()))
            )
            self.renderer.blit(
                fin_fps_font,
                (0, 0)
            )


if __name__ == '__main__':
    BallGame().run()
