import pygame
from Data import *


class Block:
    def __init__(self, value, double, n, can_click=True) -> None:
        self.value = value * n
        self.can_click = can_click
        self.double = double

    def get_value(self):
        return (self.double + 1) * self.value

    def get_neg(self):
        return self.value == -1

    def change_value(self, n, lozenge_num_is_zero):
        if self.value == -1:
            self.value = 0
        elif n == -1:
            if not lozenge_num_is_zero:
                self.value = -1
        else:
            self.value = 1 - self.value

    def _draw_rect(self, surface, size, x, y, color):
        pygame.draw.rect(surface, color, (x, y, size, size))

    def draw_lozenge(self, surface, size, x, y, color):
        x += size / 2
        y += size / 2
        offset = 3 * size / 8
        pygame.draw.polygon(
            surface,
            color,
            (
                (x, y - offset),
                (x + offset, y),
                (x, y + offset),
                (x - offset, y),
            ),
            int(round(size / 12)),
        )

    def _draw_circle(self, surface, size, x, y, color, bg):
        pygame.draw.circle(
            surface,
            color,
            (
                x + size / 2,
                y + size / 2,
            ),
            size * 3 / 8,
        )
        pygame.draw.circle(
            surface,
            bg,
            (
                x + size / 2,
                y + size / 2,
            ),
            3 * size / 10,
        )

    def _draw_double_image(self, surface, size, x, y, get_double_img):
        img = get_double_img(self.value)
        w, h = img.get_size()
        surface.blit(
            img,
            (x + (size - w) // 2, y + (size - h) // 2),
        )

    def draw(self, surface, size, x, y, get_double_img):
        if not self.can_click:
            self._draw_rect(surface, size, x, y, dark_gray)
            if self.value == -1:
                self.draw_lozenge(surface, size, x, y, blue)
            elif self.value == 1:
                self._draw_circle(surface, size, x, y, "#00000000", dark_gray)
        else:
            if self.value == -1:
                self.draw_lozenge(surface, size, x, y, blue)
            elif self.value == 1:
                self._draw_circle(surface, size, x, y, dark_gray, "#00000000")
            if self.double:
                self._draw_double_image(surface, size, x, y, get_double_img)
