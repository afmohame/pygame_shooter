import pygame
import characters_old
import math
import projectile_old
import cte_old

class Enemy(characters_old.Character):
    def __init__(self, pos, bot_stats, bot_hitbox_info, bot_sprite_info, bot_sprite_sheet, 
                 bot_animation_info, bot_animation_moves, frame, last_update, last_atk, tile_size):
        super().__init__( pos, bot_stats, bot_hitbox_info, bot_sprite_info, bot_sprite_sheet, 
                 bot_animation_info, frame, last_update)
        self.atk = bot_stats["attack"]
        self.atk_type = bot_stats["attack_type"]
        self.atk_clown = bot_stats["attack_cooldown"]
        self.bot_animation_moves = bot_animation_moves
        self.detection_range = bot_stats["detection_range"]
        self.attack_range = bot_stats["attack_range"]
        self.stop_chase_range = bot_stats["stop_range"]
        self.last_atk = last_atk
        self.bot_state = "idle"
        self.tile_size = tile_size
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))
    
    def update_tile_pos(self):
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)

        self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))

    def update(self, player, world_map, current_time):
        dx, dy = self.x - player.x, self.y - player.y
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        #Make it move with states
        if distance <= self.detection_range:

            #Make it retreat
            if distance <= self.stop_chase_range:
                self.bot_state = "retreat"
                move_x, move_y = abs(dx) > self.speed, abs(dy) > self.speed #checks if bot needs to move each axis
                if move_x and move_y:
                    speed = self.speed_xy
                else:
                    speed = self.speed
        
                if move_x:
                    if dx > 0:
                        if world_map.move_allowed((self.x + speed, self.y), (self.hitbox_width, self.hitbox_height)):
                            self.x += speed
                    else:
                        if world_map.move_allowed((self.x - speed, self.y), (self.hitbox_width, self.hitbox_height)):
                            self.x -= speed
                    
                if move_y:
                    if dy > 0:
                        if world_map.move_allowed((self.x, self.y + speed), (self.hitbox_width, self.hitbox_height)):
                            self.y += speed
                    else:
                        if world_map.move_allowed((self.x, self.y - speed), (self.hitbox_width, self.hitbox_height)):
                            self.y -= speed

            #Make it attack
            elif distance <= self.attack_range:
                self.bot_state = "attack"

                #Attack cooldown and player hp
                if current_time - self.last_atk > self.atk_clown:
                    proj = projectile_old.Projectile(self.center, "magic bullet", cte_old.proj_bot1["area"], cte_old.proj_bot1["damage"],
                                           cte_old.proj_bot1["speed"], cte_old.proj_bot1["life_time"], current_time, player.center)
                    cte_old.list_of_enemy_projectile.append(proj)
                    self.last_atk = current_time
            
            #Make it chase
            else:
                self.bot_state = "chase"
                tile_pos = world_map.find_path(self.tile_pos, player.tile_pos)
                if len(tile_pos) >= 2:
                    pixel_pos = (tile_pos[1][0]*self.tile_size + self.tile_size//2, tile_pos[1][1]*self.tile_size + self.tile_size//2)

                    #Movement logic
                    cdx, cdy = pixel_pos[0] - self.center[0], pixel_pos[1] - self.center[1]
                    move_x, move_y = abs(cdx) > self.speed, abs(cdy) > self.speed #checks if bot needs to move each axis
                    if move_x and move_y:
                        speed = self.speed_xy
                    else:
                        speed = self.speed
            
                    if move_x:
                        if cdx > 0:
                            if world_map.move_allowed((self.x + speed, self.y), (self.hitbox_width, self.hitbox_height)):
                                self.x += speed
                        else:
                            if world_map.move_allowed((self.x - speed, self.y), (self.hitbox_width, self.hitbox_height)):
                                self.x -= speed
                        
                    if move_y:
                        if cdy > 0:
                            if world_map.move_allowed((self.x, self.y + speed), (self.hitbox_width, self.hitbox_height)):
                                self.y += speed
                        else:
                            if world_map.move_allowed((self.x, self.y - speed), (self.hitbox_width, self.hitbox_height)):
                                self.y -= speed

        #Make it idle 
        else:
            self.bot_state = "idle"
        
        self.update_tile_pos()
    
    def draw_bot(self, surface, blit_image, x, y, camera):
        surface.blit(blit_image, (x - camera[0], y - camera[1]))


#projectiles
projectile_img = pygame.image.load("sprites/images_chosen_for_game/fireball.png")