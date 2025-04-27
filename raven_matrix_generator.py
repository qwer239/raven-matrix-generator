from PIL import Image, ImageDraw
import random

class RavenMatrixGenerator:
    def __init__(self, type_num=None, cell_size=150, grid_size=3):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.margin = 20
        self.W = cell_size * grid_size + self.margin * (grid_size + 1)
        self.H = cell_size * (grid_size + 1) + self.margin * (grid_size + 2)
        
        # 문제 유형 설정 (10번만 활성화)
        self.type_generators = {10: self.generate_line_combination}

    def generate_problem(self, type_num=10):
        return self.type_generators[type_num]()

    def generate_line_combination(self):
        """10번 문제: 선분 결합 패턴 (보기 A-E 포함)"""
        img = Image.new('RGB', (self.W, self.H), 'white')
        draw = ImageDraw.Draw(img)
        
        # 3x3 매트릭스 그리기
        for i in range(3):
            for j in range(3):
                x = self.margin + j * (self.cell_size + self.margin)
                y = self.margin + i * (self.cell_size + self.margin)
                draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black', width=2)
                
                # 물음표 칸
                if i == 2 and j == 2:
                    draw.text((x+self.cell_size//2-5, y+self.cell_size//2-10), '?', fill='black')
                else:
                    # 패턴 선분 그리기
                    if (i, j) == (0, 0):
                        draw.line((x+30, y+30, x+self.cell_size-30, y+self.cell_size-30), fill='black', width=3)
                    elif (i, j) == (0, 1):
                        draw.line((x+30, y+30, x+self.cell_size-30, y+30), fill='black', width=3)
        
        # 보기(A-E) 그리기
        options = [
            [(0.3, 0.3, 0.7, 0.7)],  # A: 대각선
            [(0.5, 0.3, 0.5, 0.7)],  # B: 수직선
            [(0.3, 0.5, 0.7, 0.5)],  # C: 수평선
            [(0.3, 0.3, 0.7, 0.3), (0.7, 0.3, 0.7, 0.7)],  # D: ㄱ자
            [(0.3, 0.7, 0.7, 0.7), (0.7, 0.7, 0.7, 0.3)]   # E: ㄴ자
        ]
        
        for idx, lines in enumerate(options):
            x = self.margin + idx * (self.cell_size + self.margin)
            y = self.margin*4 + self.cell_size*3  # 하단 위치
            
            # 보기 칸
            draw.rectangle((x, y, x+self.cell_size, y+self.cell_size), outline='black', width=2)
            
            # 보기 레이블(A-E)
            draw.text((x+self.cell_size//2-5, y+self.cell_size+5), chr(65+idx), fill='black')
            
            # 보기 패턴
            for line in lines:
                x1, y1, x2, y2 = line
                draw.line((
                    x + x1*self.cell_size,
                    y + y1*self.cell_size,
                    x + x2*self.cell_size,
                    y + y2*self.cell_size
                ), fill='black', width=3)
        
        return img, 'A'  # 정답: A

# 사용 예시
if __name__ == "__main__":
    generator = RavenMatrixGenerator()
    img, answer = generator.generate_problem()
    img.show()



