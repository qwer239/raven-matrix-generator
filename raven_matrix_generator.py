import numpy as np
from PIL import Image, ImageDraw
import random
import os
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
        
        # 모든 문제 유형 정의 (1~23)
        self.type_names = {
            1: "위치 패턴 (Position Pattern)",
            2: "채움 패턴 (Fill Pattern)",
            3: "코너 패턴 (Corner Pattern)",
            # ... (23번까지 유형 추가)
            22: "선분 결합 패턴 (Line Combination)",
            23: "로켓 패턴 (Rocket Pattern)"
        }
        
        # 유형별 생성 함수 매핑
        self.type_generators = {
            1: self.generate_position_pattern,
            2: self.generate_fill_pattern,
            # ... (23번까지 매핑)
            22: self.generate_line_combination,
            23: self.generate_rocket_pattern
        }

    def generate_problem(self, type_num=None):
        """지정된 유형의 문제 생성"""
        if type_num is None:
            type_num = random.choice(list(self.type_generators.keys()))
        return self.type_generators[type_num]()

    # --------------------------
    # 문제 1: 위치 패턴 (예시)
    # --------------------------
    def generate_position_pattern(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        # 패턴 구현...
        return img, 'A'

    # --------------------------
    # 문제 22: 선분 결합 패턴
    # --------------------------
    def generate_line_combination(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        
        # 패턴 데이터
        patterns = [
            [[(0.2, 0.2, 0.8, 0.8)], [(0.2, 0.2, 0.8, 0.2)], [(0.8, 0.2, 0.8, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.8, 0.8, 0.8)], [(0.2, 0.2, 0.2, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.2, 0.8, 0.8)], None]
        ]
        
        # 3x3 매트릭스 그리기
        for i in range(3):
            for j in range(3):
                x = self.margin + j * (self.cell_size + self.margin)
                y = self.margin + i * (self.cell_size + self.margin)
                if i == 2 and j == 2:
                    draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black')
                    draw.text((x+self.cell_size//2-10, y+self.cell_size//2-10), '?', fill='black')
                else:
                    self._draw_lines(draw, (x, y), patterns[i][j])
        
        # 옵션 생성
        options = [
            [[(0.2, 0.8, 0.8, 0.2), (0.2, 0.2, 0.8, 0.8)]],  # 정답: A
            [[(0.2, 0.2, 0.8, 0.8)]],  # B
            [[(0.2, 0.2, 0.5, 0.5), (0.5, 0.5, 0.8, 0.2)]],  # C
            [[(0.2, 0.2, 0.8, 0.2), (0.8, 0.2, 0.8, 0.8)]],  # D
            [[(0.2, 0.2, 0.5, 0.5), (0.5, 0.5, 0.8, 0.8)]]   # E
        ]
        
        # 옵션 그리기
        labels = ['A', 'B', 'C', 'D', 'E']
        for idx, lines in enumerate(options):
            x = self.margin + idx * (self.cell_size + self.margin)
            y = self.margin*(self.grid_size+1) + self.cell_size*self.grid_size
            self._draw_lines(draw, (x, y), lines)
        
        return img, 'A'

    # --------------------------
    # 문제 23: 로켓 패턴
    # --------------------------
    def generate_rocket_pattern(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        
        # 로켓 머리/몸통/꼬리 패턴 구현...
        return img, 'B'

    # --------------------------
    # 공통 도우미 함수들
    # --------------------------
    def _draw_lines(self, draw, pos, lines):
        """선분 그리기"""
        x, y = pos
        for line in lines:
            x1, y1, x2, y2 = line
            draw.line((
                x + x1*self.cell_size, 
                y + y1*self.cell_size,
                x + x2*self.cell_size, 
                y + y2*self.cell_size
            ), fill='black', width=3)

    def _draw_grid(self, draw):
        """3x3 격자 그리기"""
        for i in range(1, 3):
            # 수직선
            draw.line((
                self.margin + i*(self.cell_size + self.margin),
                self.margin,
                self.margin + i*(self.cell_size + self.margin),
                self.margin + 3*self.cell_size + 2*self.margin
            ), fill='gray')
            # 수평선
            draw.line((
                self.margin,
                self.margin + i*(self.cell_size + self.margin),
                self.margin + 3*self.cell_size + 2*self.margin,
                self.margin + i*(self.cell_size + self.margin)
            ), fill='gray')

    def save_as_pdf(self, problems, filename="output.pdf"):
        """PDF 저장"""
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        problems_per_page = 4
        
        for idx, (img, answer) in enumerate(problems):
            if idx % problems_per_page == 0 and idx != 0:
                c.showPage()
            
            img_path = f"temp_{idx}.png"
            img.save(img_path)
            
            x = 50 + (idx % 2) * 250
            y = height - 300 - (idx // 2 % 2) * 350
            
            c.drawImage(img_path, x, y, width=200, height=200)
            c.drawString(x+10, y-20, f"정답: {answer}")
            os.remove(img_path)
        
        c.save()

# 사용 예시
if __name__ == "__main__":
    generator = RavenMatrixGenerator()
    
    # 문제 22번 생성
    img, answer = generator.generate_problem(type_num=22)
    img.show()
    
    # PDF로 저장 (여러 문제)
    problems = [generator.generate_problem(type_num=i) for i in range(1, 24)]
    generator.save_as_pdf(problems)
