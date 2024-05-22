import pygame
import random

from Data import *
from Block import Block
from BoardBlock import BoardBlock


class LevelBoard:
    def __init__(self, data, level_double_small) -> None:
        (
            self.row_num,
            self.column_num,
            self.p_4,
            self.p_2,
            self.p_n1,
            self.difficulty,
            self.gradeup_list,
        ) = data
        self._Reset(level_double_small)
        self.lozenge_num = self.NEG_SET - self.get_neg_sum()

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

    def return_RCP_dict(self):
        return {
            "row_num": self.row_num,
            "column_num": self.column_num,
            "p_4": self.p_4,
            "p_2": self.p_2,
            "p_n1": self.p_n1,
            "difficulty": self.difficulty,
            "gradeup_list": self.gradeup_list,
        }
    
    def return_5data_tuple(self):
        return (
            self.row_num,
            self.column_num,
            self.p_4,
            self.p_2,
            self.p_n1,
        )

    @staticmethod
    def rand_bool():
        return int(random.random() < 0.6)

    def create_board(self, level_double_small) -> dict[tuple, Block]:
        return {
            (column_index, row_index): Block(
                self.rand_bool(),
                random.random() < self.p_2 / p_2_full,
                -1 if random.random() < self.p_n1 / p_n1_full else 1,
            )
            if random.random() > self.p_4 / p_4_full
            else BoardBlock(
                lambda: self.size // 2,
                level_double_small,
                self.rand_bool,
                self.p_2 / p_4_full,
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

    def click(self, n, x, y, dx, dy):
        if n == -1 and (self.NEG_SUM == 0 or self.lozenge_num < 0):
            return
        block = self.board[(x, y)]
        if isinstance(block, BoardBlock):
            block.click(dx, dy, n, self.lozenge_num == 0)
        elif block.can_click:
            block.change_value(n, self.lozenge_num == 0)

    def update_neg(self):
        if self.NEG_SUM <= 0:
            return
        lozenge_num = self.lozenge_num
        self.lozenge_num = self.NEG_SET - self.get_neg_sum()
        if lozenge_num == self.lozenge_num:
            return
        color = blue if self.lozenge_num else white_gray
        self.lozenge_num_img = self.level_ui.font.render(
            f"{self.lozenge_num}", True, color
        )

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
                color = green
            else:
                color = red
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
                color = green
            else:
                color = red
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

    def draw(self, surface, draw_data):
        self._draw_block(surface, draw_data)
        self._draw_row_lines(surface, draw_data)
        self._draw_column_lines(surface, draw_data)
        self._draw_number(surface, draw_data)
        

    def _Reset(self, level_double_small):
        self.board: dict[tuple, Block] = self.create_board(level_double_small)
        self.row_aim = [
            self.get_row_sum(row_index) for row_index in range(self.row_num)
        ]
        self.column_aim = [
            self.get_column_sum(column_index) for column_index in range(self.column_num)
        ]
        self.NEG_SUM = self.get_neg_sum()
        self.NEG_SET = int(round(self.NEG_SUM * (1 + random.random() / 3)))
        self.refresh()


    def Reset(self, level_double_small):
        self._Reset(level_double_small)

    def Recover(self):        
        self.row_num = self.column_num = 3
        self.p_4 = self.p_2 = self.p_n1 = self.difficulty = 0
        self.gradeup_list = ["row_num", "column_num"]
    
    def DifficuityGradeUp(self):
        if self.difficulty == 0:
            if max((self.row_num, self.column_num)) >= 5:
                self.difficulty += 1
                self.gradeup_list.append("p_4")
        elif self.difficulty == 1:
            if max((self.row_num, self.column_num)) >= 7 and self.p_4 >= 2:
                self.difficulty += 1
                self.gradeup_list.append("p_2")
        elif self.difficulty == 2:
            if (
                max((self.row_num, self.column_num)) >= 10
                and max((self.p_2, self.p_4)) >= 4
            ):
                self.difficulty += 1
                self.gradeup_list.append("p_n1")

    def Gradeup(self):
        if not self.gradeup_list:
            return self
        r = random.randint(0, len(self.gradeup_list) - 1)
        name = self.gradeup_list[r]
        value = getattr(self, name) + 1
        setattr(self, name, value)
        if value >= self.GRADEUP_MAX[name]:
            del self.gradeup_list[r]

        self.DifficuityGradeUp()

# LevelBoard()
