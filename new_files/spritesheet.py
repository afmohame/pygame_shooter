import pygame

class Sprites():
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