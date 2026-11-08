import pygame as pg
import sys

# Třída pro kreslení X nebo O na obrazovku
class DrawXorO:
    def __init__(self, screen):
        self.screen = screen

    def draw_x(self, x, y, size=50):
        pg.draw.line(self.screen, (255, 0, 0), (x, y), (x + size, y + size), 5)
        pg.draw.line(self.screen, (255, 0, 0), (x + size, y), (x, y + size), 5)

    def draw_o(self, x, y, radius=25):
        pg.draw.circle(self.screen, (0, 255, 0), (x + radius, y + radius), radius, 5)

# Herní logika pro kontrolu výhry a stavu mřížky
class Logic:
    def __init__(self, rows=3, colums=3):
        self.rows = rows
        self.colums = colums
        self.board = [[0 for _ in range(colums)] for _ in range(rows)]

    def make_move(self, row, col, player):
        if self.board[row][col] == 0:
            self.board[row][col] = player
            return True
        return False

    def check_winner(self, clicked_cells=[]):
        if len(clicked_cells) >= self.rows * self.colums:
            return "draw"

        # Kontrola řádků
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]

        # Kontrola sloupců
        for col in range(self.colums):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]

        # Hlavní diagonála
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]

        # Vedlejší diagonála
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

        return None

# Třída pro vykreslování a hlavní smyčku hry
class Render:
    def __init__(self, bg=(0, 0, 0), caption="Tic-tac-toe", screen_w=900, screen_h=400):
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        self.running = True
        self.bg = bg
        self.caption = caption
        self.XorO = DrawXorO(self.screen)
        self.logic = Logic(rows=3, colums=3)

    def draw_grid(self, rows=3, cols=3):
        for row in range(rows):
            for col in range(cols):
                rect = pg.Rect(col * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height)
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Vykreslení bílé mřížky

    def winner_text(self, winner):
        font = pg.font.SysFont("Arial", 74)
        if winner == "draw":
            text = font.render("Draw!", True, (255, 255, 0))
        else:
            text = font.render(f"{winner} wins!", True, (255, 255, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))

    def start_rendering(self, screen_w=900, screen_h=400):
        selected = "X"
        already_drawn = {}
        rows, cols = 3, 3
        self.cell_width = self.screen.get_width() // cols
        self.cell_height = (self.screen.get_height() // rows) - 30
        
        clicked_cells = []

        pg.display.set_caption(self.caption)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // self.cell_width
                    row = y // self.cell_height
                    
                    if 0 <= col < cols and 0 <= row < rows:
                        if (col, row) not in clicked_cells:
                            print(f"Clicked on cell: ({col}, {row})")
                            clicked_cells.append((col, row))

                            if selected == "X":
                                already_drawn[(col, row)] = "X"
                                print(f"Drawing X at cell: ({col}, {row})")
                                self.logic.make_move(row=row, col=col, player="X")
                                selected = "O"
                            elif selected == "O":
                                print(f"Drawing O at cell: ({col}, {row})")
                                already_drawn[(col, row)] = "O"
                                self.logic.make_move(row=row, col=col, player="O")
                                selected = "X"

            # Vyčištění obrazovky
            self.screen.fill(self.bg)

            # Vykreslení ohraničení a mřížky
            pg.draw.rect(self.screen, (0, 0, 255), (0, 0, self.screen.get_width(), self.screen.get_height()), 1)
            self.draw_grid(rows, cols)

            # Kontrola výhry / remízy
            winner = self.logic.check_winner(clicked_cells=clicked_cells)
            if winner is not None:
                if winner != "draw":
                    print(f"Winner is: {winner}")
                else:
                    print("Draw!")
                
                # Zobrazení textu a dvousekundová pauza před resetem
                self.winner_text(winner=winner)
                pg.display.flip()
                pg.time.delay(2000)
                
                # Reset proměnných pro nové kolo
                selected = "X"
                already_drawn = {}
                clicked_cells = []
                self.logic.board = [[0 for _ in range(cols)] for _ in range(rows)]

            # Indikace hráče na tahu
            if selected == "O":
                self.XorO.draw_o(self.screen.get_width() - 100, self.screen.get_height() - 80, radius=35)
            else:
                self.XorO.draw_x(self.screen.get_width() - 100, self.screen.get_height() - 80, size=70)

            # Vykreslení všech tahů (X a O)
            for col, row in clicked_cells:
                cell_x = col * self.cell_width
                cell_y = row * self.cell_height
                
                radius = 35
                center_x = cell_x + (self.cell_width // 2) - radius
                center_y = cell_y + (self.cell_height // 2) - radius

                if (col, row) in already_drawn:
                    if already_drawn[(col, row)] == "X":
                        self.XorO.draw_x(center_x, center_y, size=radius*2)
                    elif already_drawn[(col, row)] == "O":
                        self.XorO.draw_o(center_x, center_y, radius=radius)
        
            pg.display.flip()

        pg.quit()
        sys.exit()
