import pygame

class Sprites(pygame.sprite.Sprite):
    def __init__(self, image):#groups may be added but don't know what it does 
        #super().__init__(*groups)
        self.sheet = image

    def slice_sheet(self, frame_index, column_index, first_x, first_y, width, height, scale, transparency_color,
                    x_space, y_space):
        sprite = pygame.Surface((width, height)).convert_alpha()
        #((frame*width), 0, width, height) 2 first is cutting 
        #(0, 0)
        sprite.blit(self.sheet, (0, 0), (first_x + frame_index*x_space, first_y + column_index*y_space, width, height))
        sprite = pygame.transform.scale(sprite, (width*scale, height*scale))#scales up the image
        sprite.set_colorkey(transparency_color)#delete the excess colors
        return sprite

"""
first player sprite points to cut (as small as possible)
x1, y2 = 2, 0                (1)x-------x(2)
x2, y2 = 16, 0                  I        I 
x3, y3 = 2, 21                  I        I
x4, y4 = 16, 21              (3)x--------x(4)
width = 13
height = 23
space between sprites --> x fom 16 to 50 & y from 21 to 48
x_space = 34 + 13 = 47
y_space = 27 + 21 = 48
==> cte over hele file
"""