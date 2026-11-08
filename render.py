import pygame as pg
import sys

# Draws X or O on the screen
class DrawXorO():
    def __init__(self, screen):
        self.screen = screen

    def draw_x(self, x, y, size=50):
        pg.draw.line(self.screen, (255, 0, 0), (x, y), (x + size, y + size), 5)
        pg.draw.line(self.screen, (255, 0, 0), (x + size, y), (x, y + size), 5)

    def draw_o(self, x, y, radius=25):
        pg.draw.circle(self.screen, (0, 255, 0), (x + radius, y + radius), radius, 5)

# Renders everything on the screen
class Render:
    def __init__(self, bg=(0,0,0), caption="Tic-tac-toe", screen_w = 900, screen_h = 400):
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        self.running = True
        self.bg = bg
        self.caption = caption
        self.XorO = DrawXorO(self.screen)

    def draw_grid(self, rows=3, cols=3):
        cell_width = self.screen.get_width() // cols
        cell_height = self.screen.get_height() // rows

        for row in range(rows):
            for col in range(cols):
                if row >= rows:
                    rect = pg.Rect(col * cell_width, row * cell_height, cell_width, cell_height - 30)
                else:
                    rect = pg.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw white grid lines

    def start_rendering(self, screen_w = 900, screen_h = 400):
        rows, cols = 3, 3
        cell_width = self.screen.get_width() // cols
        cell_height = self.screen.get_height() // rows
        
        # Seznam pro uložení obsazených políček ve tvaru (col, row)
        clicked_cells = []

        pg.display.set_caption(self.caption)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Zjištění pozice myši a výpočet sloupce a řádku
                    x, y = event.pos
                    col = x // cell_width
                    row = y // cell_height
                    
                    # Pokud na tomto políčku ještě kolečko není, přidáme ho
                    if (col, row) not in clicked_cells:
                        clicked_cells.append((col, row))

            # Vyčištění obrazovky v každém snímku
            self.screen.fill(self.bg)

            # Vykreslení statického ohraničení
            pg.draw.rect(self.screen, (0, 0, 255), (0, 0, self.screen.get_width(), self.screen.get_height()), 1)

            # Vykreslení mřížky
            self.draw_grid(rows, cols)
            
            # Vykreslení koleček pro všechna kliknutá políčka
            for col, row in clicked_cells:
                cell_x = col * cell_width
                cell_y = row * cell_height
                
                # Vypočítáme střed políčka, aby byl kruh hezky uprostřed
                radius = 35
                center_x = cell_x + (cell_width // 2) - radius
                center_y = cell_y + (cell_height // 2) - radius
                
                self.XorO.draw_o(center_x, center_y, radius=radius)
        
            pg.display.flip()

        pg.quit()
        sys.exit()