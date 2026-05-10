import pygame as pg
import weapon
import math

#-----------------------------------------------
#                  constants
#-----------------------------------------------


#-----------------------------------------------
# sprite state
#-----------------------------------------------

last_update_player = pg.time.get_ticks()
last_update_bot1 = pg.time.get_ticks()
last_update_proj = pg.time.get_ticks()
animation_cooldown = 100 #miliseconds
frame = 0 

#-----------------------------------------------
# ANIMATIONS
#-----------------------------------------------
column_index = 0

#PLAYER
animation_moves_player = {"idle": 0, "up": 5, "down": 3, "left": -4, "right": 4, "dead": 9}
animation_moves_enemies = {"idle": 0, "up": 1, "down": 2, "left": 3, "right": 4}

first_x, x_space = 2, 48
first_y, y_space = 0, 48
scale = 2
column_length = 255
#animation_steps = 6 bcs there are 6 sprites for each, major, animation
animation_info = {"scale": scale, "animation_steps": 6, "column_index": 0}

#BOTS
animation_moves_enemies = {"idle": 0, "up": 0, "down": 0, "left": 0, "right": 0}
bot1_animation_info = {"scale": scale, "animation_steps": 5, "column_index": 0}
states = {"idle": 0, "attack": 1, "chase": 2, "dead": 3, "alerted": 4} #idlesheet, attacksheet, chasesheet, deadsheet

bot1_column_length = 144
bot1_fx, bot1_x_space = 0, 32
bot1_fy, bot1_y_space = 0, 0

#-----------------------------------------------
# player
#-----------------------------------------------
pos = (60, 60)
speed_player = 4
char_stat = {
    "hp": 30,
    "defense": 10,
    "speed": speed_player,
    "speed_xy": speed_player/math.hypot(speed_player, speed_player),
    "stamina": 100,
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
center_char = (pos[0] + sprite_w_h[0]//2, pos[1] + sprite_w_h[1]//2)

#-----------------------------------------------
# enemies
#-----------------------------------------------
bot_pos = (60, 60)#temporary
speed_bot1 = 3
last_atk = 0
bot1_stats = {
    "hp": 10,
    "attack": 1,
    "attack_type": "magic bullet",
    "defense": 15,
    "speed": speed_bot1,
    "speed_xy": speed_bot1/math.sqrt(2),
    "detection_range": 900,
    "attack_cooldown": 200,
    "attack_range": 410,
    "stop_range": 170
}

bot1_hitbox_info = {
    "hitbox_width": 17,
    "hitbox_height": 19,
    "hitbox_color": (255, 0, 0),
}

bot1_sprite_info = {
    "sprite_player_width": 17,
    "sprite_player_height": 18,
}
bot1_w_h = (bot1_sprite_info["sprite_player_width"]*scale, bot1_sprite_info["sprite_player_height"]*scale)
center_bot1 = (pos[0] + bot1_w_h[0]//2, pos[1] + bot1_w_h[1]//2)

#-----------------------------------------------
# guns
#-----------------------------------------------
center = (
    scale*sprite_info["sprite_player_width"]/2,
    scale*sprite_info["sprite_player_height"]/2,
)
gun_info = {"sprite_w": 22, "sprite_h": 18, "center": (22/2, 18/2), "damage": 3, "speed": 7, "area": 8, "life_time": 1600}
revolver_speed = 6
radius = sprite_info["sprite_player_height"]/2
orbit_xy = (sprite_info["sprite_player_height"]*1.5, 0)

#-----------------------------------------------
# projectiles
#-----------------------------------------------
proj_bot1 = {
    "damage": 2,
    "speed": 7,
    "area": 16,
    "life_time": 1600,
}

#-----------------------------------------------
# world
#-----------------------------------------------
world_dim = (60, 50)
tile_size = (55, 55)

#-----------------------------------------------
# OTHERS
#-----------------------------------------------
black, bg = (0, 0, 0), (100, 100, 100)#grey
fps = 60
screen_w, screen_h = 1500, 900
list_of_players, list_of_enemies, list_of_guns = [], [], []
list_of_player_projectile = []
list_of_enemy_projectile = []
camera_pos = (0, 0)

screen = pg.display.set_mode((screen_w, screen_h))
#animation preload
