import pygame
import random
from Data import *
from Block import Block


class BoardBlock:
    def __init__(self, get_size, levelDouble, v_randon, p_4, p_n1) -> None:
        """p_4 is real, random.random() < p_4"""
        self.get_size = get_size
        self.levelDouble = levelDouble
        self.board = {
            (0, 0): Block(
                v_randon(), random.random() < p_4, -1 if random.random() < p_n1 else 1
            ),
            (1, 0): Block(
                v_randon(), random.random() < p_4, -1 if random.random() < p_n1 else 1
            ),
            (0, 1): Block(
                v_randon(), random.random() < p_4, -1 if random.random() < p_n1 else 1
            ),
            (1, 1): Block(
                v_randon(), random.random() < p_4, -1 if random.random() < p_n1 else 1
            ),
        }

    @property
    def size(self):
        return self.get_size()

    def get_neg(self):
        return sum(block.get_neg() for block in self.board.values())

    def get_all_sum(self):
        return sum(block.get_value() for block in self.board.values())

    def get_value(self):
        return self.get_all_sum()

    def refresh(self):
        for block in self.board.values():
            # if random.random() < 0.2:
            #     block.can_click = False
            # else:
            #     block.value = False
            if not block.value and random.random() < 0.75:
                block.can_click = False
            else:
                block.value = 0

    def click(self, x, y, n, lozenge_num_is_zero):
        x = int(x // self.size > 0)
        y = int(y // self.size > 0)
        block = self.board[(x, y)]
        if block.can_click:
            block.change_value(n, lozenge_num_is_zero)

    def _draw_block(self, surface, x, y):
        for pos, block in self.board.items():
            block.draw(
                surface,
                self.size,
                pos[0] * self.size + x,
                pos[1] * self.size + y,
                self.levelDouble.get_double_img,
            )

    def _draw_lines(self, surface, x, y):
        pygame.draw.line(
            surface,
            "black",
            (x, y + self.size),
            (x + 2 * self.size, y + self.size),
            round(self.size * 0.06),
        )
        pygame.draw.line(
            surface,
            "black",
            (x + self.size, y),
            (x + self.size, y + 2 * self.size),
            round(self.size * 0.06),
        )

    def draw(self, surface, x, y):
        """x, y 是像素位置"""
        self._draw_block(surface, x, y)
        self._draw_lines(surface, x, y)
