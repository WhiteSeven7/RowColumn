import pygame
from Data import *


class LevelUI:
    def __init__(self, get_data, cheating) -> None:
        self.get_data = get_data
        self.cheating = cheating
        self.will_cheating = False
        self._reset_display()

    def _reset_value(self):
        row_num, column_num, p_4, p_2, p_n1 = self.get_data()
        self.row_image = self.font.render(f"行:{row_num}", True, black)
        self.column_image = self.font.render(f"列:{column_num}", True, black)
        self.p_4_image = self.font.render(f"田:{p_4 * 100 / p_4_full:.0f}%", True, black)
        self.p_2_image = self.font.render(f"双:{p_2 * 100 / p_2_full:.0f}%", True, black)
        self.p_n1_image = self.font.render(f"负:{p_n1 * 100 / p_n1_full:.0f}%", True, blue)

    def reset_value(self):
        return self._reset_value()

    def _reset_display(self):
        w, h = pygame.display.get_window_size()
        self.font = pygame.font.Font(
            "res/milky-mono-cn-normal.ttf", int(round(min((w, h)) / 30))
        )
        self.F4_image = self.font.render("F4:全屏", True, black)
        self.R_image = self.font.render("R:换一个", True, black)
        self.N_image = self.font.render("N:从头开始", True, black)
        self.Z_image = self._get_z_image(
            white_gray if not self.cheating else black
        )

        self.zuojian_image = self.font.render("左键画圈", True, black)
        self.youjian_image = self.font.render("右键菱形", True, blue)
        self.zaici_image = self.font.render("再按取消", True, dark_gray)

        self._reset_value()

    def reset_display(self):
        self._reset_display()

    def _draw_left_top(self, surface, x, y, data_3):
        p_4, p_2, p_n1 = data_3
        surface.blit(self.row_image, (x, y))
        y += self.row_image.get_height()
        surface.blit(self.column_image, (x, y))
        y += self.column_image.get_height()
        if p_4:
            surface.blit(self.p_4_image, (x, y))
            y += self.p_4_image.get_height()
        if p_2:
            surface.blit(self.p_2_image, (x, y))
            y += self.p_2_image.get_height()
        if p_n1:
            surface.blit(self.p_n1_image, (x, y))

    def _draw_left_buttom(self, surface, x, y, p_n1):
        y -= self.zaici_image.get_height()
        surface.blit(self.zaici_image, (x, y))
        if p_n1:
            y -= self.youjian_image.get_height()
            surface.blit(self.youjian_image, (x, y))
        y -= self.zuojian_image.get_height()
        surface.blit(self.zuojian_image, (x, y))

    def _draw_RNC(self, surface, w, h):
        surface.blit(
            self.F4_image,
            (w / 5 - self.F4_image.get_width() / 2, h - self.F4_image.get_height()),
        )
        surface.blit(
            self.R_image,
            (2 * w / 5 - self.R_image.get_width() / 2, h - self.R_image.get_height()),
        )
        surface.blit(
            self.N_image,
            (3 * w / 5 - self.N_image.get_width() / 2, h - self.N_image.get_height()),
        )
        surface.blit(
            self.Z_image,
            (4 * w / 5 - self.Z_image.get_width() / 2, h - self.Z_image.get_height()),
        )

    def draw(self, surface, win_size):
        w, h = win_size
        x = y = int(round(min((w, h)) / 40))
        data = self.get_data()
        self._draw_left_top(surface, x, y, data[2:])
        self._draw_left_buttom(surface, x, h * 0.85, data[-1])
        self._draw_RNC(surface, w, h * 0.98)

    def set_cheating(self):
        self.cheating = True
        self.Z_image = self._get_z_image(black)

    def romove_cheating(self):
        self.cheating = False
        self.Z_image = self._get_z_image(white_gray)

    def _get_z_image(self, color):
        return self.font.render("Z:直接过关", True, color)
