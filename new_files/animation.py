import pygame as pg
import spritesheet as sps
import cte
import character as char

###  LOADING SPRITES ###
player_spritesheet = pg.image.load("sprites/images_chosen_for_game/player.png")
play_quit = {"play": pg.image.load("sprites/images_chosen_for_game/buttons/play_unpressed.png"),
        "play_pressed": pg.image.load("sprites/images_chosen_for_game/buttons/play_pressed.png"), 
        "quit": pg.image.load("sprites/images_chosen_for_game/buttons/quit_unpressed.png"),
        "quit_pressed": pg.image.load("sprites/images_chosen_for_game/buttons/quit_pressed.png")}

###  PLAYER  ###
player = sps.Sprites(player_spritesheet)
player_animations = {
    "idle": player.animation(cte.animation_info["frames"], cte.animation_moves_player["idle"], 
                                  cte.first_x, cte.first_y, cte.player_info["sprite"][0], cte.player_info["sprite"][1], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),

    "run_front": player.animation(cte.animation_info["frames"], cte.animation_moves_player["up"], 
                                  cte.first_x, cte.first_y, cte.player_info["sprite"][0], cte.player_info["sprite"][1], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),

    "run_Lside": player.animation(cte.animation_info["frames"], cte.animation_moves_player["left"], 
                                  cte.first_x, cte.first_y, cte.player_info["sprite"][0], cte.player_info["sprite"][1], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),

    "run_Rside": player.animation(cte.animation_info["frames"], cte.animation_moves_player["right"], 
                                  cte.first_x, cte.first_y, cte.player_info["sprite"][0], cte.player_info["sprite"][1], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),

    "run_down": player.animation(cte.animation_info["frames"], cte.animation_moves_player["down"],
                                 cte.first_x, cte.first_y, cte.player_info["sprite"][0], cte.player_info["sprite"][1], 
                                 cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
}
""""dead": player.animation(3, cte.animation_moves_player["dead"], cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                   cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length//2),"""


###  BOT1  ###
bot1_idle = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/bot1_idle.png"))
bot1_walking = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/bot1_walking.png"))
bot1_atk = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/bot1_atk.png"))
bot1_animations = {
    "idle": bot1_idle.animation(cte.bot1_animation_info["idle"]["frames"], 0, cte.bot1_animation_info["idle"]["first_x"], cte.bot1_animation_info["idle"]["first_y"],
                                cte.bot1_animation_info["idle"]["sprite"][0], cte.bot1_animation_info["idle"]["sprite"][1], cte.scale, cte.black,
                                cte.bot1_animation_info["idle"]["x_space"], cte.bot1_animation_info["idle"]["y_space"], cte.bot1_animation_info["idle"]["sheet_width"]),

    "walking": bot1_walking.animation(cte.bot1_animation_info["walking"]["frames"], 0, cte.bot1_animation_info["walking"]["first_x"], cte.bot1_animation_info["walking"]["first_y"],
                                cte.bot1_animation_info["walking"]["sprite"][0], cte.bot1_animation_info["walking"]["sprite"][1], cte.scale, cte.black,
                                cte.bot1_animation_info["walking"]["x_space"], cte.bot1_animation_info["idle"]["y_space"], cte.bot1_animation_info["walking"]["sheet_width"]),

    "attack": bot1_atk.animation(cte.bot1_animation_info["attack"]["frames"], 0, cte.bot1_animation_info["attack"]["first_x"], cte.bot1_animation_info["idle"]["first_y"],
                                cte.bot1_animation_info["attack"]["sprite"][0], cte.bot1_animation_info["attack"]["sprite"][1], cte.scale, cte.black,
                                cte.bot1_animation_info["attack"]["x_space"], cte.bot1_animation_info["idle"]["y_space"], cte.bot1_animation_info["attack"]["sheet_width"]),
}
###  BOT2  ###
bot2_idle = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot2_idle.png"))
bot2_atk = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot2_attack.png"))
bot2_walking = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot2_movement.png"))
bot2_td = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot2_take_damage.png"))
bot2_dead = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot2_death.png"))
bot2_animations = {
    "idle": bot2_idle.animation(cte.bot2_animation_info["idle"]["frames"], 0, cte.bot2_animation_info["idle"]["first_x"], cte.bot2_animation_info["idle"]["first_y"],
                                cte.bot2_animation_info["idle"]["sprite"][0], cte.bot2_animation_info["idle"]["sprite"][1], cte.scale, cte.black, 
                                cte.bot2_animation_info["idle"]["x_space"], cte.bot2_animation_info["idle"]["y_space"], cte.bot2_animation_info["idle"]["sheet_width"]),

    "walking": bot2_walking.animation(cte.bot2_animation_info["walking"]["frames"], 0, cte.bot2_animation_info["walking"]["first_x"], cte.bot2_animation_info["walking"]["first_y"], 
                                   cte.bot2_animation_info["walking"]["sprite"][0], cte.bot2_animation_info["walking"]["sprite"][1], cte.scale, cte.black, 
                                   cte.bot2_animation_info["walking"]["x_space"], cte.bot2_animation_info["walking"]["y_space"], cte.bot2_animation_info["walking"]["sheet_width"]),

    "attack": bot2_atk.animation(cte.bot2_animation_info["attack"]["frames"], 0, cte.bot2_animation_info["attack"]["first_x"], cte.bot2_animation_info["walking"]["first_y"], 
                                  cte.bot2_animation_info["attack"]["sprite"][0], cte.bot2_animation_info["attack"]["sprite"][1], cte.scale, cte.black, 
                                  cte.bot2_animation_info["attack"]["x_space"], cte.bot2_animation_info["attack"]["y_space"], cte.bot2_animation_info["attack"]["sheet_width"]),

    "dead": bot2_dead.animation(cte.bot2_animation_info["death"]["frames"], 0, cte.bot2_animation_info["death"]["first_x"], cte.bot2_animation_info["walking"]["first_y"], 
                                cte.bot2_animation_info["death"]["sprite"][0], cte.bot2_animation_info["death"]["sprite"][1], cte.scale, cte.black, 
                                cte.bot2_animation_info["death"]["x_space"], cte.bot2_animation_info["death"]["y_space"], cte.bot2_animation_info["death"]["sheet_width"]),

    "take_damage": bot2_td.animation(cte.bot2_animation_info["take_damage"]["frames"], 0, cte.bot2_animation_info["take_damage"]["first_x"], cte.bot2_animation_info["take_damage"]["first_y"], 
                                       cte.bot2_animation_info["take_damage"]["sprite"][0], cte.bot2_animation_info["take_damage"]["sprite"][1], cte.scale, cte.black, 
                                       cte.bot2_animation_info["take_damage"]["x_space"], cte.bot2_animation_info["take_damage"]["y_space"], cte.bot2_animation_info["take_damage"]["sheet_width"]),
}

"""
### BOT3 ###
bot3_idle = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot3_idle.png"))
bot3_atk = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot3_attack.png"))
bot3_movement = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot3_movement.png"))
bot3_td = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot3_take_damage.png"))
bot3_dead = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/enemy/bot3_death.png"))

bot3_animations = {
    "idle": bot3_idle.animatio,
    "walking": bot3_idle.animatio,
    "attack": bot3_idle.animatio,
    "dead": bot3_idle.animatio,
    "take_damage": bot3_idle.animatio,
}
"""
### WEAPONS/PROJECTILES ###
revolver = pg.image.load("sprites/images_chosen_for_game/revolver.png")
kogel = pg.transform.rotate(pg.image.load("sprites/images_chosen_for_game/bullet1.png"), 90)

fireball = pg.image.load("sprites/images_chosen_for_game/fireball.png")
