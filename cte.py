import pygame as pg
import weapon
#import main

#-----------------------------------------------
#                  constants
#-----------------------------------------------


#-----------------------------------------------
# sprite state
#-----------------------------------------------

last_update = pg.time.get_ticks()
animation_cooldown = 100 #miliseconds
frame = 0 


#-----------------------------------------------
# ANIMATIONS
#-----------------------------------------------
animation_moves = {"idle": 0, "up": 5, "down": 3, "left": -4, "right": 4, "dead": 9}

column_index = 0

first_x, x_space = 2, 48
first_y, y_space = 0, 48
scale = 2
column_length = 255

#animation_steps = 6 bcs there are 6 sprites for each, major, animation
animation_info = {"scale": scale, "animation_steps": 6, "column_index": 0} 


#-----------------------------------------------
# player
#-----------------------------------------------
pos = (60, 60)
char_stat = {
    "hp": 30,
    "defense": 10,
    "speed": 4,
    "stamina": 10,
}

hitbox_info = {
    "hitbox_width": 11,
    "hitbox_height": 22,
    "hitbox_color": (255, 0, 0),
}

sprite_info = {
    "sprite_player_width": 14,
    "sprite_player_height": 21,
}
sprite_w_h = (sprite_info["sprite_player_width"]*scale, sprite_info["sprite_player_height"]*scale)
center_char = (pos[0] + sprite_info["sprite_player_width"]*scale//2, pos[1] + sprite_info["sprite_player_height"]*scale//2)
#-----------------------------------------------
# guns
#-----------------------------------------------
center = (
    scale*sprite_info["sprite_player_width"]/2,
    scale*sprite_info["sprite_player_height"]/2,
)

revolver_speed = 6
radius = sprite_info["sprite_player_height"]/2
orbit_xy = (sprite_info["sprite_player_height"]*1.5, 0)

#-----------------------------------------------
# world
#-----------------------------------------------
world_dim = (100, 70)
tile_size = (55, 55)

#-----------------------------------------------
# OTHERS
#-----------------------------------------------
black, bg = (0, 0, 0), (100, 100, 100)#grey
fps = 60
screen_w, screen_h = 1500, 900
list_of_players, list_of_enemies, list_of_guns = [], [], []
camera_pos = (0, 0)

#animation preload
