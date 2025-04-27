import numpy as np
from PIL import Image, ImageDraw
import random
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class RavenMatrixGenerator:
    def __init__(self, type_num=None, difficulty=3, cell_size=120, grid_size=3):
        self.type_num = type_num
        self.difficulty = difficulty
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.margin = 10
        self.W = cell_size*grid_size + self.margin*(grid_size+1)
        self.H = cell_size*grid_size + self.margin*(grid_size+1) + cell_size + 3*self.margin
        
        # 유형 분류 및 이름
        self.type_names = {
            1: "위치 패턴 (Position Pattern)",
            2: "채움 패턴 (Fill Pattern)",
            3: "기하 변환 (Geometric Transformation)",
            4: "요소 진행 (Element Progression)",
            5: "영역 패턴 (Region Pattern)",
            6: "점 패턴 (Point Pattern)",
            7: "심볼 배치 (Symbol Arrangement)",
            8: "상태 변환 (State Transformation)",
            9: "로켓/우산 패턴 (Rocket/Umbrella Pattern)",
            10: "선분 결합 패턴 (Line Combination Pattern)",
            11: "회전 삭제 패턴 (Rotation Subtraction Pattern)"
        }
        
        # 유형별 문제 생성기 함수 매핑
        self.type_generators = {
            1: [self.generate_position_pattern],
            2: [self.generate_fill_pattern, self.generate_state_cycle],
            3: [self.generate_corner_pattern, self.generate_shape_combination],
            4: [self.generate_line_rotation, self.generate_grid_pattern],
            5: [self.generate_dual_region, self.generate_diamond_pattern],
            6: [self.generate_vertex_movement],
            7: [self.generate_quadrant_symbol, self.generate_line_dot_pattern],
            8: [self.generate_shape_state, self.generate_umbrella_pattern],
            9: [self.generate_rocket_pattern],  # 문제 #23
            10: [self.generate_star_line_pattern],  # 문제 #22
            11: [self.generate_rotation_subtraction_pattern]  # 문제 #24
        }

    def generate_problem(self):
        """요청한 유형에서 무작위로 패턴 선택하여 문제 생성"""
        if self.type_num is None:
            self.type_num = random.choice(list(self.type_generators.keys()))
        if self.type_num not in self.type_generators:
            raise ValueError(f"지원되지 않는 문제 유형: {self.type_num}")
        
        # 해당 유형에서 무작위로 생성 함수 선택
        generator = random.choice(self.type_generators[self.type_num])
        return generator()

    # 예시 문제 생성 함수 (문제 #22: 선분 결합 패턴)
    def generate_star_line_pattern(self):
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        
        patterns = [
            [[(0.2, 0.2, 0.8, 0.8)], [(0.2, 0.2, 0.8, 0.2)], [(0.8, 0.2, 0.8, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.8, 0.8, 0.8)], [(0.2, 0.2, 0.2, 0.8)]],
            [[(0.2, 0.8, 0.8, 0.2)], [(0.2, 0.2, 0.8, 0.8)], None]
        ]
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = self.margin + j*(self.cell_size + self.margin)
                y = self.margin + i*(self.cell_size + self.margin)
                
                if patterns[i][j] is None:
                    draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black', width=1)
                    draw.text((x+self.cell_size//2-5, y+self.cell_size//2-10), '?', fill='black')
                else:
                    self._draw_lines_pattern(draw, (x, y), patterns[i][j])
        
        options = [
            [[(0.2, 0.8, 0.8, 0.2), (0.2, 0.2, 0.8, 0.8)]],  # A
            [[(0.2, 0.2, 0.8, 0.8)]],  # B
            [[(0.2, 0.2, 0.5, 0.5), (0.5, 0.5, 0.8, 0.2)]],  # C
            [[(0.2, 0.2, 0.8, 0.2), (0.2, 0.2, 0.2, 0.8), (0.8, 0.2, 0.8, 0.8), (0.2, 0.8, 0.8, 0.8)]],  # D
            [[(0.2, 0.2, 0.8, 0.2), (0.8, 0.2, 0.8, 0.8), (0.8, 0.8, 0.2, 0.8), (0.2, 0.8, 0.2, 0.2)]]  # E
        ]
        
        labels = ['A', 'B', 'C', 'D', 'E']
        answer_idx = 0
        
        for idx, lines in enumerate(options):
            x = self.margin + idx*(self.cell_size + self.margin)
            y = self.margin*(self.grid_size+1) + self.cell_size*self.grid_size
            self._draw_lines_pattern(draw, (x, y), lines)
            draw.text((x+self.cell_size//2-5, y+self.cell_size+5), labels[idx], fill='black')
        
        return img, labels[answer_idx]

    def _draw_lines_pattern(self, draw, pos, lines):
        x, y = pos
        s = self.cell_size
        for line in lines:
            x1, y1, x2, y2 = line
            draw.line((x + x1*s, y + y1*s, x + x2*s, y + y2*s), fill='black', width=2)

# 추가 문제 생성 함수 및 도형 그리기 함수는 위와 같은 방식으로 구현

print("RavenMatrixGenerator 클래스 구조 및 일부 예시 코드 제공 완료")
