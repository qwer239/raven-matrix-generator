from PIL import Image, ImageDraw
import random

class RavenMatrixGenerator:
    def __init__(self, type_num=None, difficulty=3, cell_size=150, grid_size=3):
        self.type_num = type_num
        self.difficulty = difficulty
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.margin = 10
        self.W = cell_size * grid_size + self.margin * (grid_size + 1)
        self.H = cell_size * grid_size + self.margin * (grid_size + 1) + cell_size + 3 * self.margin
        
        # 문제 10번만 활성화
        self.type_generators = {10: self.generate_line_combination}

    def generate_problem(self, type_num=None):
        return self.generate_line_combination()

    def generate_line_combination(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        
        # 3x3 매트릭스 그리기
        for i in range(3):
            for j in range(3):
                x = self.margin + j * (self.cell_size + self.margin)
                y = self.margin + i * (self.cell_size + self.margin)
                draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black')
                
                if i == 2 and j == 2:
                    draw.text((x+self.cell_size//2-5, y+self.cell_size//2-10), '?', fill='black')
                else:
                    if i == 0 and j == 0:
                        draw.line((x+20, y+20, x+self.cell_size-20, y+self.cell_size-20), fill='black', width=3)
                    elif i == 0 and j == 1:
                        draw.line((x+20, y+20, x+self.cell_size-20, y+20), fill='black', width=3)
                    elif i == 0 and j == 2:
                        draw.line((x+self.cell_size-20, y+20, x+self.cell_size-20, y+self.cell_size-20), fill='black', width=3)
        
        # 보기(A-E) 추가
        for idx in range(5):
            x = self.margin + idx * (self.cell_size + self.margin)
            y = self.margin*(self.grid_size+1) + self.cell_size*self.grid_size
            draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black')
            draw.text((x+self.cell_size//2-5, y+self.cell_size//2-10), chr(65+idx), fill='black')
        
        return img, 'A'


