import pygame
from Data import *

class LevelDouble:
    def __init__(self, size) -> None:
        double_font = pygame.font.Font(
            "res/milky-mono-cn-normal.ttf", int(round(size * 0.4))
        )
        self.img = double_font.render("2", True, white_gray)
        self.img_black = double_font.render("+2", True, dark_gray)
        self.img_blue = double_font.render("-2", True, blue)

    def reset(self, size):
        self.__init__(size)

    def get_double_img(self, value):
        if value == -1:
            img = self.img_blue
        elif value == 1:
            img = self.img_black
        else:
            img = self.img
        return img