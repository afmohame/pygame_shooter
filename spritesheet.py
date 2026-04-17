import pygame

class Animations():#probably won't use it
    def __init__(self):
        pass

class Sprites(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):#groups may be added but don't know what it does 
        #super().__init__(*groups)
        self.sprite_sheet = sprite_sheet

    def slice_sheet(self, surface, animation_steps, column_index, first_x, first_y, width, height, scale, transparency_color,
                    x_space, y_space):
        surface_sprites = pygame.Surface((width, height)).convert_alpha()#this is for one signel sprite frame
        if column_index < 0:
            surface_sprites.blit(surface, (0, 0), (first_x + animation_steps*x_space, first_y, width, height))
            sprite = pygame.transform.scale(surface_sprites, (width*scale, height*scale))#scales up the image
            flipped_sprite = pygame.transform.flip(sprite, True, False)
            flipped_sprite.set_colorkey(transparency_color)#delete the excess colors
            return flipped_sprite

        surface_sprites.blit(surface, (0, 0), (first_x + animation_steps*x_space, first_y, width, height))
        sprite = pygame.transform.scale(surface_sprites, (width*scale, height*scale))#scales up the image
        sprite.set_colorkey(transparency_color)#delete the excess colors
        return sprite

    def animation(self, animation_steps, column_index, first_x, first_y, width, height, scale, transparency_color,
                  x_space, y_space, column_length):
        animation_list = []
        surface = pygame.Surface((column_length, height)).convert_alpha()#creates a rectangle surface with width as x distance and height as y distance
        surface.blit(self.sprite_sheet, (0, 0), (first_x, first_y + abs(column_index)*y_space, column_length, height))
        for i in range(animation_steps):
            sliced_sprites = self.slice_sheet(surface, i, column_index, first_x, first_y, width, height, scale, transparency_color, x_space, y_space)
            animation_list.append(sliced_sprites)
        return animation_list
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


self.sheet = the sprite sheet you want to use
(0, 0) = means on the sprite surface, blit the image on this sprite surface on coordinate (0, 0
(first_x + frame_index*x_space, first_y + column_index*y_space, width, height) = coordinates 
    --> first_x + frame_index*x_space = x-coordinate where to begin ON THE SPRITESHEET and the index of the row with the space between each sprite
    --> first_y + column_index*y_space = y-coordinate where to begin ON THE SPRITESHEET  and the index of the column with the space between each sprite
    --> width, height = the length of the sprite in x and y direction ON THE SPRITESHEET 
"""