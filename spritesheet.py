import pygame

class Sprites(pygame.sprite.Sprite):
    def __init__(self, image):#groups may be added but don't know what it does 
        #super().__init__(*groups)
        self.sheet = image
        self.xpace = 33 #temporary for player
        self.yspace = 25 #temporary for player

    def get_image(self, frame, width, height, scale, color, x_space = None, yspace = None):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame*width), 0, width, height))#sheet, coordinate image, area
        image = pygame.transform.scale(image, (width*scale, height*scale))#scales up the image
        image.set_colorkey(color)
        return image

"""
first player sprite points to cut (as small as possible)
x1, y2 = 2, 0                (1)x-------x(2)
x2, y2 = 17, 0                  I        I 
x3, y3 = 2, 23                  I        I
x4, y4 = 17, 23              (3)x--------x(4)
width = 15
height = 23
space between sprites --> x fom 17 to 50 & y from 23 to 48
x_space = 33
yspace = 25
==> cte over hele file
"""