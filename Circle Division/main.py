import pygame as pg
import numpy as np
from settings import *

pg.init()
screen = pg.display.set_mode((SCREEN, SCREEN))
screen.fill("white")
clock = pg.time.Clock()

class Game():
    def __init__(self) -> None:
        self.center = [SCREEN//2, SCREEN//2]
        self.plus_image = pg.image.load('Circle Division/images/plus_sign.jpg').convert_alpha()
        self.plus_image = pg.transform.scale(self.plus_image, (20,20))
        self.minus_image = pg.image.load('Circle Division/images/minus_sign.jpg').convert_alpha()
        self.minus_image = pg.transform.scale(self.minus_image, (20,20))
        self.plus_a = self.create_button(self.plus_image, [SCREEN-SCREEN/10 + 10, SCREEN/20 + 50])
        self.minus_a = self.create_button(self.plus_image, [SCREEN-SCREEN/10 - 30, SCREEN/20 + 50])

        self.divisions = 500
        self.a = 2
        self.space = np.linspace(0, 2*np.pi, self.divisions)
        self.setup()


    def setup(self):
        self.reset = False
        self.x = [i for i in range(1,self.divisions+1,1)]
        pg.draw.circle(screen, "black", self.center, RADIUS, width=1)
        self.pointsx = [self.rad_to_cart(i) for i in self.space]

        font = pg.font.SysFont("Arial", 25)
        self.a_text = font.render("a = " + str(self.a), True, "black")
        
        self.running = True
        self.loop()

    def create_button(self, img, pos):
        rect = img.get_rect()
        rect.topleft = pos
        return rect
    
    def mod_division(self, point):
        return (self.a * point) % self.divisions

    def rad_to_cart(self, ang):
        return [sum(x) for x in zip(self.center, [RADIUS*np.cos(ang), RADIUS*np.sin(ang)])]
    
    def point_to_coord(self, point):
        return self.rad_to_cart(self.space[point-1])

    def loop(self):
        while(self.running):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONUP:
                    if self.plus_a.collidepoint(event.pos):
                        self.a += 1
                        self.reset = True
                    if self.minus_a.collidepoint(event.pos):
                        if self.a == 2:
                            pass
                        else:
                            self.a -=1
                            self.reset=True

            self.update()
            self.draw()
            if self.reset:
                screen.fill("white")
                self.setup()
            pg.display.flip()
            clock.tick(FPS)
    
    def update(self):
        for i in self.x:
            pg.draw.line(screen, "black", self.point_to_coord(i), self.point_to_coord(self.mod_division(i)))
    
    def draw(self):
        screen.blit(self.a_text, (SCREEN - SCREEN/10 - 30, SCREEN/20))
        screen.blit(self.plus_image, (self.plus_a.x, self.plus_a.y))
        screen.blit(self.minus_image, (self.minus_a.x, self.minus_a.y))

g = Game()
pg.quit()