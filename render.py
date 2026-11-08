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
class Logic():
    def __init__(self, colums=3, rows=3):
        self.colums = colums
        self.rows = rows
        self.board = {}  # Initialize the board with empty rows
        for row in range(rows):
            if not self.board.get("rowsX"):
                self.board["rowsX"] = []
            if not self.board.get("rowsO"):
                self.board["rowsO"] = []
            self.board["rowsX"].append(int("0") * rows)  # Each row is a list of 0 values
            self.board["rowsO"].append(int("0") * rows)  # Each row is a list of 0 values
        for col in range(colums):
            if not self.board.get("columsX"):
                self.board["columsX"] = []
            if not self.board.get("columsO"):
                self.board["columsO"] = []
            self.board["columsX"].append(int("0") * colums)  # Each colum is a list of 0 values
            self.board["columsO"].append(int("0") * colums)  # Each colum is a list of 0 values
           
        print(f"Initialized board: {self.board}")

    def incrementTable(self, selected, row, col):
        if selected == "X":
            self.board["rowsX"][row] += 1
            self.board["columsX"][col] += 1
        elif selected == "O":
            self.board["rowsO"][row] -= 1
            self.board["columsO"][col] -= 1
        print(f"Updated board: {self.board}")
    def check_winner(self):
        for key in self.board.keys():
            for value in self.board[key]:
                if value == 1:
                    return "X"
                elif value == -1:
                    return "O"
# Renders everything on the screen
class Render:
    def __init__(self, bg=(0,0,0), caption="Tic-tac-toe", screen_w = 900, screen_h = 400):
        pg.init()
        self.screen = pg.display.set_mode((screen_w, screen_h))
        self.running = True
        self.bg = bg
        self.caption = caption
        self.XorO = DrawXorO(self.screen)
        self.logic = Logic()
    def draw_grid(self, rows=3, cols=3):
        cell_width = self.screen.get_width() // cols
        cell_height = self.screen.get_height() // rows

        for row in range(rows):
            for col in range(cols):
                if row >= rows:
                    rect = pg.Rect(col * cell_width, row * cell_height, cell_width, cell_height - 50)
                else:
                    rect = pg.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw white grid lines

    def start_rendering(self, screen_w = 900, screen_h = 400):
        selected = "X"
        already_drawn = {}
        rows, cols = 3, 3
        self.cell_width = self.screen.get_width() // cols
        self.cell_height = self.screen.get_height() // rows

        
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
                    col = x // self.cell_width
                    row = y // self.cell_height
                    
                    # Pokud na tomto políčku ještě kolečko není, přidáme ho
                    if (col, row) not in clicked_cells:
                        print(f"Clicked on cell: ({col}, {row})")
                        clicked_cells.append((col, row))

                    if not (col, row) in already_drawn:
                        if selected == "X":
                            already_drawn[(col, row)] = "X"
                            print(f"Drawing X at cell: ({col}, {row})")
                            self.logic.incrementTable(selected, row, col)
                            selected = "O"
                        elif selected == "O":
                            print(f"Drawing O at cell: ({col}, {row})")
                            already_drawn[(col, row)] = "O"
                            self.logic.incrmentTable(selected, row, col)
                            selected = "X"

            # Vyčištění obrazovky v každém snímku
            self.screen.fill(self.bg)

            # Vykreslení statického ohraničení
            pg.draw.rect(self.screen, (0, 0, 255), (0, 0, self.screen.get_width(), self.screen.get_height()), 1)

            # Vykreslení mřížky
            self.draw_grid(rows, cols)
            
            # Vykreslení koleček pro všechna kliknutá políčka
            for col, row in clicked_cells:
                cell_x = col * self.cell_width
                cell_y = row * self.cell_height
                
                # Vypočítáme střed políčka, aby byl kruh hezky uprostřed
                radius = 35
                center_x = cell_x + (self.cell_width // 2) - radius
                center_y = cell_y + (self.cell_height // 2) - radius
                if (col, row) in already_drawn and already_drawn[(col, row)] == "X":
                    self.XorO.draw_x(center_x, center_y, size=radius*2)
                    selected = "O"  # Přepnutí na O po vykreslení X
                elif (col, row) in already_drawn and already_drawn[(col, row)] == "O":
                    self.XorO.draw_o(center_x, center_y, radius=radius)
                    selected = "X"  # Přepnutí na X po vykreslení O
        
            pg.display.flip()

        pg.quit()
        sys.exit()