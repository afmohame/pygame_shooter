import pygame as pg
import characters

class Collision(characters.Position):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def botsing(self, andereFiguur):
        if(isinstance(self,Cirkel)): #x,y is midden van de cirkel en voor de botsing willen we linker en rechter bovenhoek.
            x1 = self.x-self.radius
            y1 = self.y-self.radius
            x2 = self.x + self.radius
            y2 = self.y + self.radius
        else: #voor een rechthoek is x en y de linkerbovenhoek
            x1 = self.x
            y1 = self.y
            x2 = self.x + self.breedte
            y2 = self.y + self.hoogte
        if(isinstance(andereFiguur,Cirkel)):
            andereFiguurx1 = andereFiguur.x-andereFiguur.radius
            andereFiguury1 = andereFiguur.y-andereFiguur.radius
            andereFiguurx2 = andereFiguur.x + andereFiguur.radius
            andereFiguury2 = andereFiguur.y + andereFiguur.radius
        else:
            andereFiguurx1 = andereFiguur.x
            andereFiguury1 = andereFiguur.y
            andereFiguurx2 = andereFiguur.x + andereFiguur.breedte
            andereFiguury2 = andereFiguur.y + andereFiguur.hoogte
# https://silentmatt.com/rectangle-intersection/
        if x1 < andereFiguurx2 and x2 > andereFiguurx1 and y1 < andereFiguury2 and y2 > andereFiguury1:
            return True
        else:
            return False
