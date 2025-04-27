import numpy as np
from PIL import Image, ImageDraw
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class RavenMatrixGenerator:
    def __init__(self, type_num=None, difficulty=3, cell_size=150, grid_size=3):
        self.type_num = type_num
        self.difficulty = difficulty
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.margin = 10
        self.W = cell_size * grid_size + self.margin * (grid_size + 1)
        self.H = cell_size * grid_size + self.margin * (grid_size + 1) + cell_size + 3 * self.margin

        # 문제 10번(선분 결합 패턴)만 임시로 활성화
        self.type_generators = {
            10: self.generate_line_combination
        }

    def generate_problem(self, type_num=None):
        if type_num is None:
            type_num = 10
        return self.type_generators[type_num]()

    def generate_line_combination(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        patterns = [
            [[(0.2, 0.2, 0.8, 0.8)], [(0.2, 0.2, 0.8, 0.2)], [(0.8, 0.2, 0.8, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.8, 0.8, 0.8)], [(0.2, 0.2, 0.2, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.2, 0.8, 0.8)], None]
        ]
        for i in range(3):
            for j in range(3):
                x = self.margin + j * (self.cell_size + self.margin)
                y = self.margin + i * (self.cell_size + self.margin)
                if i == 2 and j == 2:
                    draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black')
                    draw.text((x+self.cell_size//2-10, y+self.cell_size//2-10), '?', fill='black')
                else:
                    self._draw_lines(draw, (x, y), patterns[i][j])
        return img, 'A'

    def _draw_lines(self, draw, pos, lines):
        x, y = pos
        for line in lines:
            x1, y1, x2, y2 = line
            draw.line((
                x + x1*self.cell_size, 
                y + y1*self.cell_size,
                x + x2*self.cell_size, 
                y + y2*self.cell_size
            ), fill='black', width=3)

