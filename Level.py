import pygame
import random
import json

from Data import *
from LevelBoard import LevelBoard
from LevelDouble import LevelDouble
from LevelUI import LevelUI
from Block import Block
from BoardBlock import BoardBlock


class Level:
    def __init__(self) -> None:
        data = self.get_RCP("res/data.json")
        # 游戏
        self.size = self.get_size(data[0], data[1])
        # 2的图像
        self.level_double = LevelDouble(self.size)
        self.level_double_small = LevelDouble(self.size / 2)

        (
            self.row_num,
            self.column_num,
            self.p_4,
            self.p_2,
            self.p_n1,
            self.difficulty,
            self.gradeup_list,
            cheating,
        ) = data
        self.board: dict[tuple, Block | BoardBlock] = self.create_board()
        self.row_aim = [
            self.get_row_sum(row_index) for row_index in range(self.row_num)
        ]
        self.column_aim = [
            self.get_column_sum(column_index) for column_index in range(self.column_num)
        ]
        self.NEG_SUM = self.get_neg_sum()
        self.NEG_SET = int(round(self.NEG_SUM * (1 + random.random() / 3)))
        self.refresh()
        # 菱形数量
        self.lozenge_num = self.NEG_SET - self.get_neg_sum()

        # 位置
        win_size = pygame.display.get_window_size()
        self._set_board_pos(win_size)
        self.font = pygame.font.Font(
            "res/milky-mono-cn-normal.ttf", int(round(self.size * 0.6))
        )
        # 动画
        self.canvas = pygame.Surface(win_size).convert_alpha()
        self.anim_tick = 0
        self.ANIM_TIME = 45
        self.alpha = 255
        self.offset_x = 0
        self.offset_y = 0
        self.OFFSET_X = min(self.left, self.size * 3 / 2)
        self.OFFSET_Y = min(self.top, self.size * 3 / 2)
        # UI
        self.level_ui = LevelUI(lambda:(self.row_num, self.column_num, self.p_4, self.p_2, self.p_n1), cheating)
        # 菱形图像
        self.lozenge_num_img = self.level_ui.font.render(
            f"{self.lozenge_num}", True, blue
        )

        self.new_game = False
        self.win = False
        # 难度
        self.GRADEUP_MAX = self.get_GRADEUP_MAX()

    def _set_board_pos(self, win_size):
        w, h = win_size
        self.left = (w - self.size * self.column_num) // 2
        self.top = (h - self.size * self.row_num) // 2
        self.right = w - self.left
        self.bottom = h - self.top

    @staticmethod
    def get_RCP(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data["row_num"],
            data["column_num"],
            data["p_4"],
            data["p_2"],
            data["p_n1"],
            data["difficulty"],
            data["gradeup_list"],
            data["cheating"],
        )

    def write_RCP(self, file_path):
        data = {
            "row_num": self.row_num,
            "column_num": self.column_num,
            "p_4": self.p_4,
            "p_2": self.p_2,
            "p_n1": self.p_n1,
            "difficulty": self.difficulty,
            "gradeup_list": self.gradeup_list,
            "cheating": self.level_ui.cheating
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_GRADEUP_MAX(self):
        with open("res/MAX.json", "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_size(row_num, column_num):
        w_size = min(pygame.display.get_window_size())
        b_size = max((row_num, column_num)) + 2
        return int(w_size * 0.8 / b_size)

    def get_row_sum(self, row_index: int) -> int:
        return sum(
            self.board[(column_index, row_index)].get_value()
            for column_index in range(self.column_num)
        )

    def get_column_sum(self, column_index: int) -> int:
        return sum(
            self.board[(column_index, row_index)].get_value()
            for row_index in range(self.row_num)
        )

    def get_all_sum(self) -> int:
        return sum(
            self.get_column_sum(column_index) for column_index in range(self.column_num)
        )

    def check_all(self) -> bool:
        return all(
            self.get_column_sum(column_index) == self.column_aim[column_index]
            for column_index in range(self.column_num)
        ) and all(
            self.get_row_sum(row_index) == self.row_aim[row_index]
            for row_index in range(self.row_num)
        )

    def quit(self):
        self.write_RCP("res/data.json")

    @staticmethod
    def rand_bool():
        return int(random.random() < 0.6)

    def create_board(self) -> dict[tuple, Block]:
        return {
            (column_index, row_index): Block(
                self.rand_bool(),
                random.random() < self.p_2 / p_2_full,
                -1 if random.random() < self.p_n1 / p_n1_full else 1,
            )
            if random.random() > self.p_4 / p_4_full
            else BoardBlock(
                lambda: self.size // 2,
                self.level_double_small,
                self.rand_bool,
                self.p_2 / p_2_full,
                self.p_n1 / p_n1_full,
            )
            for row_index in range(self.row_num)
            for column_index in range(self.column_num)
        }

    def get_neg_sum(self):
        return sum(block.get_neg() for block in self.board.values())

    def refresh(self):
        for block in self.board.values():
            if isinstance(block, BoardBlock):
                block.refresh()
                continue

            # if random.random() < 0.2:
            #     block.can_click = False
            # else:
            #     block.value = False
            if not block.value and random.random() < 0.6:
                block.can_click = False
            else:
                block.value = 0

    def Entry(self) -> "Level":
        self.anim_tick = -self.ANIM_TIME
        return self

    def Working(self) -> "Level":
        self.anim_tick = 0
        self.alpha = 255
        self.offset_x = 0
        self.offset_y = 0
        return self

    def finished(self) -> bool:
        return self.anim_tick >= self.ANIM_TIME

    def DifficuityGradeUp(self):
        if self.difficulty == 0:
            if max((self.row_num, self.column_num)) >= 4:
                self.difficulty += 1
                self.gradeup_list.append("p_4")
        elif self.difficulty == 1:
            if max((self.row_num, self.column_num)) >= 6 and self.p_4 >= 2:
                self.difficulty += 1
                self.gradeup_list.append("p_2")
        elif self.difficulty == 2:
            if (
                max((self.row_num, self.column_num)) >= 8
                and max((self.p_2, self.p_4)) >= 4
            ):
                self.difficulty += 1
                self.gradeup_list.append("p_n1")

    def Gradeup_(self) -> "Level":
        if not self.gradeup_list:
            return self
        r = random.randint(0, len(self.gradeup_list) - 1)
        name = self.gradeup_list[r]
        value = getattr(self, name) + 1
        setattr(self, name, value)
        if value >= self.GRADEUP_MAX[name]:
            del self.gradeup_list[r]

        self.DifficuityGradeUp()
        return self
    
    def Gradeup(self) -> "Level":
        return self.Gradeup_().Gradeup_().Gradeup_().Gradeup_()

    def do_when_change_size(self, win_size):
        # 位置
        self._set_board_pos(win_size)
        self.font = pygame.font.Font(
            "res/milky-mono-cn-normal.ttf", int(round(self.size * 0.6))
        )
        # 动画
        self.OFFSET_X = min(self.left, self.size * 3 / 2)
        self.OFFSET_Y = min(self.top, self.size * 3 / 2)
        # 2的图像
        self.level_double.reset(self.size)
        self.level_double_small.reset(self.size / 2)
        # UI
        self.level_ui.reset_value()

    def do_when_change_display(self, win_size):
        w, h = pygame.display.get_window_size()
        # 动画
        self.canvas = pygame.Surface((w, h)).convert_alpha()
        # UI
        self.level_ui.reset_display()
        # 菱形图像
        self.lozenge_num_img = self.level_ui.font.render(
            f"{self.lozenge_num}", True, blue
        )

        self.do_when_change_size(win_size)

    def ResetWhenFullscreen(self) -> "Level":
        self.size = self.get_size(self.row_num, self.column_num)
        self.do_when_change_display(pygame.display.get_window_size())
        return self

    def Recover(self):
        self.row_num = self.column_num = 4
        self.p_4 = self.p_2 = self.p_n1 = self.difficulty = 0
        self.gradeup_list = ["row_num", "column_num"]
        self.level_ui.romove_cheating()
        return self

    def Reset(self) -> "Level":
        # 游戏
        self.size = self.get_size(self.row_num, self.column_num)
        self.board: dict[tuple, Block] = self.create_board()
        self.row_aim = [
            self.get_row_sum(row_index) for row_index in range(self.row_num)
        ]
        self.column_aim = [
            self.get_column_sum(column_index) for column_index in range(self.column_num)
        ]
        self.NEG_SUM = self.get_neg_sum()
        self.NEG_SET = int(round(self.NEG_SUM * (1 + random.random() / 3)))
        self.refresh()

        self.do_when_change_size(pygame.display.get_window_size())
        # Tool
        return self

    def key_down(self, key):
        if key == pygame.K_z:
            self.anim_tick = self.ANIM_TIME
            self.win = True
            self.level_ui.set_cheating()
        if key == pygame.K_r:
            self.anim_tick += 1
        elif key == pygame.K_n:
            self.anim_tick += 1
            self.new_game = True

    def click(self, pos, n):
        if self.anim_tick != 0:
            return
        x, y = pos
        x, dx = divmod(x - self.left, self.size)
        y, dy = divmod(y - self.top, self.size)
        if x < 0 or x >= self.column_num or y < 0 or y >= self.row_num:
            return
        
        if n == -1 and (self.NEG_SUM == 0 or self.lozenge_num < 0):
            return
        block = self.board[(x, y)]
        if isinstance(block, BoardBlock):
            block.click(dx, dy, n, self.lozenge_num == 0)
        elif block.can_click:
            block.change_value(n, self.lozenge_num == 0)

    def _update_neg(self):
        lozenge_num = self.lozenge_num
        self.lozenge_num = self.NEG_SET - self.get_neg_sum()
        if lozenge_num == self.lozenge_num:
            return
        color = blue if self.lozenge_num else white_gray
        self.lozenge_num_img = self.level_ui.font.render(
            f"{self.lozenge_num}", True, color
        )

    def normal_update(self):
        if self.check_all():
            self.anim_tick += 1

    def check_change(self):
        if self.finished():
            if self.win:  # Z
                self.win = False
                self.Gradeup().Reset().Working()
            elif self.new_game:  # N
                self.new_game = False
                self.Recover().Reset().Entry()
            elif self.check_all():  # 正常通关
                self.Gradeup().Reset().Entry()
            else:  # R
                self.Reset().Entry()

    def check_anim_tick(self):
        if self.anim_tick == 0:
            self.normal_update()
            return
        self.anim_tick += 1
        if self.anim_tick == 0:
            self.alpha = 255
            self.offset_x = 0
            self.offset_y = 0
        else:
            self.alpha = 255 - round(abs(self.anim_tick) * 255 / self.ANIM_TIME)
            self.offset_x = round(self.anim_tick * self.OFFSET_X / self.ANIM_TIME)
            self.offset_y = round(self.anim_tick * self.OFFSET_Y / self.ANIM_TIME)

    def update(self):
        if self.NEG_SUM > 0:
            self._update_neg()
        self.check_anim_tick()
        self.check_change()

    def _draw_block(self, surface):
        for pos, block in self.board.items():
            x, y = self.left + pos[0] * self.size, self.top + pos[1] * self.size
            if isinstance(block, BoardBlock):
                block.draw(surface, x, y)
            else:
                block.draw(surface, self.size, x, y, self.level_double.get_double_img)

    def _draw_row_lines(self, surface):
        for row_index in range(self.row_num + 1):
            pygame.draw.line(
                surface,
                "black",
                (self.left + self.offset_x, self.top + self.size * row_index),
                (
                    self.left + self.size * self.column_num + self.offset_x,
                    self.top + self.size * row_index,
                ),
                round(self.size * 0.06),
            )

    def _draw_column_lines(self, surface):
        for column_index in range(self.column_num + 1):
            pygame.draw.line(
                surface,
                "black",
                (self.left + self.size * column_index, self.top + self.offset_y),
                (
                    self.left + self.size * column_index,
                    self.top + self.size * self.row_num + self.offset_y,
                ),
                round(self.size * 0.06),
            )

    def _draw_number_top(self, surface):
        for column_index, num in enumerate(self.column_aim):
            num_image = self.font.render(str(num), True, white_gray)
            w, h = num_image.get_size()
            x = self.left + column_index * self.size + (self.size - w) // 2
            y = self.top - (self.size + h) // 2
            surface.blit(num_image, (x, y))

    def _draw_number_left(self, surface):
        for row_index, num in enumerate(self.row_aim):
            num_image = self.font.render(str(num), True, white_gray)
            w, h = num_image.get_size()
            x = self.left - (self.size + w) // 2
            y = self.top + row_index * self.size + (self.size - h) // 2
            surface.blit(num_image, (x, y))

    def _draw_number_down(self, surface):
        for column_index, num in enumerate(self.column_aim):
            column_sum = self.get_column_sum(column_index)
            if column_sum < num:
                color = dark_gray
            elif column_sum == num:
                color = "#22B14C"
            else:
                color = "#ED1C24"
            num_image = self.font.render(str(column_sum), True, color)
            w, h = num_image.get_size()
            x = self.left + column_index * self.size + (self.size - w) // 2
            y = self.top + self.row_num * self.size + (self.size - h) // 2
            surface.blit(num_image, (x, y))

    def _draw_number_right(self, surface):
        for row_index, num in enumerate(self.row_aim):
            row_sum = self.get_row_sum(row_index)
            if row_sum < num:
                color = dark_gray
            elif row_sum == num:
                color = "#22B14C"
            else:
                color = "#ED1C24"
            num_image = self.font.render(str(row_sum), True, color)
            w, h = num_image.get_size()
            x = self.left + self.column_num * self.size + (self.size - w) // 2
            y = self.top + row_index * self.size + (self.size - h) // 2
            surface.blit(num_image, (x, y))

    def _draw_number(self, surface):
        self._draw_number_top(surface)
        self._draw_number_left(surface)
        self._draw_number_down(surface)
        self._draw_number_right(surface)

    def _draw_neg_img(self, surface, win_size):
        w, h = win_size
        w -= w / 60
        h //= 2
        w0, h0 = self.lozenge_num_img.get_size()
        surface.blit(
            self.lozenge_num_img,
            (w - (self.size + w0) / 2, h + (self.size - h0) / 2),
        )

        color = blue if self.lozenge_num != 0 else white_gray
        block = self.board[(0, 0)]
        if isinstance(block, BoardBlock):
            block = block.board[(0, 0)]
        block.draw_lozenge(
            surface,
            self.size,
            w - self.size,
            h - self.size,
            color,
        )

    def draw(self, surface):
        win_size = pygame.display.get_window_size()
        self.canvas.fill("#00000000")
        self._draw_block(self.canvas)
        self._draw_row_lines(self.canvas)
        self._draw_column_lines(self.canvas)
        self._draw_number(self.canvas)
        if self.NEG_SUM:
            self._draw_neg_img(self.canvas, win_size)
        self.level_ui.draw(self.canvas, win_size)
        self.canvas.set_alpha(self.alpha)
        surface.blit(self.canvas, (0, 0))
