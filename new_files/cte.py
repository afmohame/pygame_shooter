import pygame as pg
import math

#-----------------------------------------------
#                  constants
#-----------------------------------------------


#-----------------------------------------------
# game variables
#-----------------------------------------------
game = "start" #start, playing, paused
#game_paused = False

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
animation_info = {"scale": scale, "frames": 6, "column_index": 0}

#BOTS
### BOT1 ###
bot1_animation_info = {
    "idle": {
        "frames": 6,
        "x_space": 32,
        "y_space": 0,
        "sprite": (12, 17),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 172
    },

    "walking": {
        "frames": 8,
        "x_space": 32,
        "y_space": 0,
        "sprite": (13,19),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 256
    },

    "attack": {
        "frames": 5,
        "x_space": 31,
        "y_space": 0,
        "sprite": (15,18),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 144
    }
}

### BOT2 ###
bot2_animation_info = {
    "idle": {
        "frames": 6,
        "x_space": 32,
        "y_space": 0,
        "sprite": (32, 32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 192
    },

    "walking": {
        "frames": 10,
        "x_space": 32,
        "y_space": 0,
        "sprite": (32,32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 320
    },

    "attack": {
        "frames": 9,
        "x_space": 32,
        "y_space": 0,
        "sprite": (32,32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 288
    },

    "take_damage": {
            "frames": 5,
            "x_space": 32,
            "y_space": 0,
            "sprite": (32,32),
            "first_x": 0,
            "first_y": 0,
            "sheet_width": 160
    },

    "death": {
            "frames": 17,
            "x_space": 32,
            "y_space": 0,
            "sprite": (32,32),
            "first_x": 0,
            "first_y": 0,
            "sheet_width": 544
        }

}

### BOT3 ###
bot3_animation_info = {
    "idle": {
        "frames": 6,
        "x_space": 0,
        "y_space": 0,
        "sprite": (32, 32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 192
    },

    "walking": {
        "frames": 10,
        "x_space": 0,
        "y_space": 0,
        "sprite": (32,32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 320
    },

    "attack": {
        "frames": 15,
        "x_space": 0,
        "y_space": 0,
        "sprite": (32,32),
        "first_x": 0,
        "first_y": 0,
        "sheet_width": 480
    },

    "take_damage": {
            "frames": 5,
            "x_space": 0,
            "y_space": 0,
            "sprite": (32,32),
            "first_x": 0,
            "first_y": 0,
            "sheet_width": 160
    },

    "death": {
            "frames": 17,
            "x_space": 0,
            "y_space": 0,
            "sprite": (32,32),
            "first_x": 0,
            "first_y": 0,
            "sheet_width": 544
        }

}

#-----------------------------------------------
# player
#-----------------------------------------------
pos = (60, 60)
player_info = {
    "hp": 30,
    "defense": 10,
    "speed": 4,
    "speed_xy": 4/math.sqrt(2),
    "stamina": 100,
    "hitbox": (11, 22),
    "hitbox_offset": (0, 0),
    "sprite": (14, 21),
}

sprite_w_h = (player_info["sprite"][0]*scale, player_info["sprite"][1]*scale)
center_char = (pos[0] + sprite_w_h[0]//2, pos[1] + sprite_w_h[1]//2)

#-----------------------------------------------
# enemies
#-----------------------------------------------
bot_pos = (200, 200)#temporary
### BOT1 ###
last_atk_bot1 = 0
bot1_info = {
    "hp": 10,
    "attack": 1,
    "attack_type": "ranged",
    "defense": 15,
    "speed": 3,
    "speed_xy": 3/math.sqrt(2),
    "detection_range": 900,
    "attack_cooldown": 600,
    "attack_range": 410,
    "stop_range": 170,
    "hitbox": (12,19),
    "hitbox_offset": (0, 0),
    "color": (255, 0, 0),
    "sprite": (32, 32),
    "projectile": {"damage": 2, "speed": 7, "life_time": 1100, "area": (16, 16), "type": "fire magic"}

}

### BOT2 ###
last_atk_bot2 = 0
bot2_info = {
    "hp": 20,
    "attack": 2,
    "attack_type": "melee",
    "defense": 15,
    "speed": 4,
    "speed_xy": 4/math.sqrt(2),
    "detection_range": 400,
    "attack_cooldown": 300,
    "attack_range": 25,
    "stop_range": 0,
    "hitbox": (12,19),
    "hitbox_offset": (7, 13),
    "color": (255, 0, 0),
    "sprite": (32, 32),
    "projectile": None

}
hitbox_bot2 = (12)

### BOT3 ###
last_atk_bot3 = 0
bot3_info = {
    "hp": 10,
    "attack": 1,
    "attack_type": "melee",
    "defense": 15,
    "speed": 3,
    "speed_xy": 3/math.sqrt(2),
    "detection_range": 900,
    "attack_cooldown": 600,
    "attack_range": 410,
    "stop_range": 170,
    "hitbox": (12,19),
    "hitbox_offset": (7, 13),
    "color": (255, 0, 0),
    "sprite": (32, 32),
    "projectile": {"damage": 2, "speed": 7, "life_time": 1100, "area": (16, 16), "type": "fire magic"}

}

bot3_w_h = (bot3_info["sprite"][0]*scale, bot3_info["sprite"][1]*scale)
center_bot3 = (pos[0] + bot3_w_h[0]//2, pos[1] + bot3_w_h[1]//2)

#-----------------------------------------------
# guns
#-----------------------------------------------
revolver = {
    "sprite_w_h": (22, 18), 
    "center": (22/2, 18/2), 
    "projectile":{"damage": 3, "speed": 7, "life_time": 1000, "area": (8, 6), "type": "bullet"} # area: width, height
}
orbit = (10, 0)
#-----------------------------------------------
# projectiles
#-----------------------------------------------
fireball = {
    "damage": 2,
    "speed": 7,
    "area": (16, 16),
    "life_time": 1100,
    "type": "fire magic",
}
guns_projectile = [revolver["projectile"], fireball]

#-----------------------------------------------
# world
#-----------------------------------------------
world_dim = (30, 30)#world_dim = (60, 50)
tile_size = (55, 55)

floor = pg.transform.scale(pg.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/06_Dungeon_Tileset.png"), tile_size)
outer_walls = pg.transform.scale(pg.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/00_right_outer_wall.png"), tile_size)
destr_wall = pg.transform.scale(pg.image.load("sprites/images_chosen_for_game/column_sprite.png"), tile_size)


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
