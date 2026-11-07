import pygame as pg
import sys

class Render:
    def __init__(self, bg=(0,0,0), caption="Tic-tac-toe"):
        pg.init()
        self.screen = pg.display.set_mode((900, 400))
        self.running = True
        self.bg = bg
        self.caption = caption
    def start_rendering(self):
        pg.display.set_caption(self.caption)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            self.screen.fill((self.bg))

            pg.draw.rect(self.screen, (0, 0, 255), (0, 0, 900, 400), 1)
            
            pg.display.flip()
        pg.quit()
        sys.exit()