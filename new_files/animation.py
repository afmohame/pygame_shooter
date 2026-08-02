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
    "idle": player.animation(cte.animation_info["animation_steps"], cte.animation_moves_player["idle"], 
                                  cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
    "run_front": player.animation(cte.animation_info["animation_steps"], cte.animation_moves_player["up"], 
                                  cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
    "run_Lside": player.animation(cte.animation_info["animation_steps"], cte.animation_moves_player["left"], 
                                  cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
    "run_Rside": player.animation(cte.animation_info["animation_steps"], cte.animation_moves_player["right"], 
                                  cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                  cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
    "run_down": player.animation(cte.animation_info["animation_steps"], cte.animation_moves_player["down"],
                                 cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                 cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length),
}
""""dead": player.animation(3, cte.animation_moves_player["dead"], cte.first_x, cte.first_y, cte.sprite_info["width"], cte.sprite_info["height"], 
                                   cte.scale, cte.black,  cte.x_space, cte.y_space, cte.column_length//2),"""


###  BOT1  ###
bot1_idle = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/bot1_idle.png"))
bot1_walking = sps.Sprites(pg.image.load("sprites/images_chosen_for_game/bot1_walking.png"))
bot1_animations = {
    "idle": bot1_idle.animation(cte.bot1_animation_info["animation_steps"], 0, cte.bot1_fx, cte.bot1_fy,
                                cte.bot1_hitbox_info["width"], cte.bot1_hitbox_info["height"], cte.scale, cte.black,
                                cte.bot1_x_space, cte.bot1_y_space, cte.bot1_column_length),
    "walking": bot1_walking.animation(cte.bot1_animation_info["animation_steps"], 0, cte.bot1_fx, cte.bot1_fy,
                                      cte.bot1_hitbox_info["width"], cte.bot1_hitbox_info["height"], cte.scale, cte.black,
                                      cte.bot1_x_space, cte.bot1_y_space, cte.bot1_column_length),
}
###  BOT2  ###


### WEAPONS/PROJECTILES ###
revolver = pg.image.load("sprites/images_chosen_for_game/revolver.png")
kogel = pg.transform.rotate(pg.image.load("sprites/images_chosen_for_game/bullet1.png"), 90)

fireball = pg.image.load("sprites/images_chosen_for_game/fireball.png")
