from PIL import Image, ImageDraw, ImageFont
import random
import os

class RavenMatrixGenerator:
    def __init__(self, cell_size=120, grid_size=3):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.margin = 20
        # 이미지 크기 계산 (3x3 그리드 + 1줄 보기)
        self.W = self.cell_size*self.grid_size + self.margin*(self.grid_size+1)
        self.H = self.cell_size*(self.grid_size+1) + self.margin*(self.grid_size+2)
        
        # 문제 유형 매핑 (10번만 활성화)
        self.type_generators = {10: self.generate_line_combination}

    def generate_problem(self, type_num=10):
        return self.type_generators[type_num]()

    def generate_line_combination(self):
        """문제 10번: 선분 결합 패턴 (보기 A-E 포함)"""
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 18)  # 글꼴 설정
        
        # 메인 3x3 그리드
        for i in range(3):
            for j in range(3):
                x = self.margin + j*(self.cell_size + self.margin)
                y = self.margin + i*(self.cell_size + self.margin)
                draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black', width=2)
                
                # 물음표 칸
                if i == 2 and j == 2:
                    draw.text((x+self.cell_size//2-5, y+self.cell_size//2-10), '?', fill='black', font=font)
                else:
                    # 패턴 선분
                    if (i, j) == (0, 0):
                        draw.line((x+30, y+30, x+self.cell_size-30, y+self.cell_size-30), fill='black', width=3)
                    elif (i, j) == (0, 1):
                        draw.line((x+30, y+30, x+self.cell_size-30, y+30), fill='black', width=3)
        
        # 보기(A-E) 영역
        options_y = self.margin*4 + self.cell_size*3  # 메인 그리드 아래 위치
        
        # 보기 패턴 데이터
        options = [
            [(0.3, 0.3, 0.7, 0.7)],  # A: 대각선
            [(0.5, 0.3, 0.5, 0.7)],  # B: 수직선
            [(0.3, 0.5, 0.7, 0.5)],  # C: 수평선
            [(0.3, 0.3, 0.7, 0.3), (0.7, 0.3, 0.7, 0.7)],  # D: ㄱ자
            [(0.3, 0.7, 0.7, 0.7), (0.7, 0.7, 0.7, 0.3)]   # E: ㄴ자
        ]
        
        # 보기 그리기
        for idx, lines in enumerate(options):
            x = self.margin + idx*(self.cell_size + self.margin)
            
            # 보기 셀
            draw.rectangle((x, options_y, x+self.cell_size, options_y+self.cell_size), outline='black', width=2)
            
            # 패턴 선분
            for line in lines:
                x1, y1, x2, y2 = line
                draw.line((
                    x + x1*self.cell_size, 
                    options_y + y1*self.cell_size,
                    x + x2*self.cell_size, 
                    options_y + y2*self.cell_size
                ), fill='black', width=3)
            
            # 레이블(A-E)
            draw.text(
                (x + self.cell_size//2 - 5, options_y + self.cell_size + 10),
                chr(65+idx), fill='black', font=font
            )
        
        return img, 'A'  # 정답: A

# 테스트 코드
if __name__ == "__main__":
    generator = RavenMatrixGenerator(cell_size=150)
    img, answer = generator.generate_problem()
    img.show()




