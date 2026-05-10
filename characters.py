import pygame as pg
import spritesheet


class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y
        
class Character(Position):
    def __init__(self, pos, char_stat, hitbox_info, sprite_info, sprite_sheet, 
                 animation_info, frame, last_update):
        super().__init__(pos[0], pos[1])
        self.sprite_sheet = spritesheet.Sprites(sprite_sheet)
        self.hp = char_stat["hp"]
        self.defense = char_stat["defense"]
        self.speed = char_stat["speed"]
        self.speed_xy = char_stat["speed_xy"]
        self.scale = animation_info["scale"]
        self.animation_steps = animation_info["animation_steps"]
        self.column_index = animation_info["column_index"]
        self.hitbox_width = hitbox_info["hitbox_width"]*self.scale
        self.hitbox_height = hitbox_info["hitbox_height"]*self.scale
        self.hitbox_color = hitbox_info["hitbox_color"]  #temporary
        self.sprite_player_width = sprite_info["sprite_player_width"] 
        self.sprite_player_height = sprite_info["sprite_player_height"]
        self.animation_seq = []
        self.frame = frame
        self.last_update = last_update
            
    def make_animation(self, transparancy_color, first_x, first_y, x_space, y_space, column_length):
        #0 is the frame I want to use, width/height is  the height of the sprites box, scale is multiplier to make it bigger
        self.animation_seq = self.sprite_sheet.animation(self.animation_steps, self.column_index, first_x, first_y, self.sprite_player_width, 
                                                         self.sprite_player_height, self.scale, transparancy_color, x_space, y_space, column_length)
        
    def get_frame(self, current_time, animation_cooldown):
        if current_time - self.last_update >= animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_seq):
                self.frame = 0 

    def get_animation(self):
        #self.length_animation_list = len(self.animation_seq) 
        return self.animation_seq[self.frame]
    
    def draw_char(self, surface, blit_image, x, y, camera):
        surface.blit(blit_image, (x - camera[0], y - camera[1]))

    def draw_hitbox(self, surface, camera):
        pg.draw.rect(surface, self.hitbox_color, rect=(self.x - camera[0], self.y - camera[1], (self.hitbox_width), 
                                                           (self.hitbox_height)))