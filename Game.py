import pygame
import sys


from Data import *
from Level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("移动的艺术")
        pygame.display.set_icon(pygame.image.load("res/icon.png"))
        self.fullscreen = False
        self.display = pygame.display.set_mode(display_size, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        pygame.mixer.init()
        self.level = Level().Entry()
        self._music_play()

    @staticmethod
    def _music_play():
        pygame.mixer.music.load("res/finger-puppets-dance.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

    def _quit(self):
        self.level.quit()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
        sys.exit()

    def change_full_screen(self):
        self.fullscreen = not self.fullscreen
        self.display = (
            pygame.display.set_mode(
                pygame.display.get_desktop_sizes()[0],
                pygame.FULLSCREEN | pygame.SRCALPHA,
            )
            if self.fullscreen
            else pygame.display.set_mode(display_size, pygame.SRCALPHA)
        )
        self.level.ResetWhenFullscreen()

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit()
                elif event.key == pygame.K_F4:
                    self.change_full_screen()
                else:
                    self.level.key_down(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.level.click(event.pos, 1)
                elif event.button == 3:
                    self.level.click(event.pos, -1)

    def update(self):
        self.level.update()

    def draw(self):
        self.display.fill(bg_color)
        self.level.draw(self.display)

        pygame.display.flip()

    def run(self):
        while True:
            self.control()
            self.update()
            self.draw()

            self.clock.tick(FPS)
