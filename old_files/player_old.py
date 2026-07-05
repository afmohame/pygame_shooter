import pygame
import world_old
import characters_old

class Player(characters_old.Character):
    def __init__(self, pos, char_stat, hitbox_info, sprite_info, sprite_sheet, 
                 animation_info, animation_moves, frame, last_update, tile_size, power_up = (None, None)):
        super().__init__(pos, char_stat, hitbox_info, sprite_info, sprite_sheet, animation_info, frame, last_update)
        self.stamina = char_stat["stamina"]
        self.animation_moves = animation_moves
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]
        self.speedier = True
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_size = tile_size
        self.tile_pos = (int(self.center[0]//tile_size), int(self.center[1]//tile_size))
    
    def update_tile_pos(self):
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)

        self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))

    def moving(self, world_map):
        keys = pygame.key.get_pressed()
        self.column_index = self.animation_moves["idle"] #column index for resting sprite

    # regenerate stamina when not holding shift
        if not keys[pygame.K_LSHIFT] and self.stamina < 100:
            self.stamina += 1

    # enable sprint again when stamina is full
        if self.stamina >= 100:
            self.speedier = True
            self.stamina = 100

    # disable sprint when stamina is empty
        if self.stamina <= 0:
            self.speedier = False
            self.stamina = 0

    # sprinting
        if keys[pygame.K_LSHIFT] and self.speedier:
            self.speed = 6
            self.stamina -= 1
        else:
            self.speed = 4


        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if world_map.move_allowed((self.x - self.speed, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["up"]
                    self.x -= self.speed_xy
                    self.y -= self.speed_xy
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if world_map.move_allowed((self.x + self.speed, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["up"]
                    self.x += self.speed_xy
                    self.y -= self.speed_xy
            if world_map.move_allowed((self.x, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["up"]
                self.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if world_map.move_allowed((self.x - self.speed, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["down"]
                    self.x -= self.speed_xy
                    self.y += self.speed_xy
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if world_map.move_allowed((self.x + self.speed, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["down"]
                    self.x += self.speed_xy
                    self.y += self.speed_xy
            if world_map.move_allowed((self.x, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["down"]
                self.y += self.speed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if world_map.move_allowed((self.x - self.speed, self.y), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["left"]
                self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if world_map.move_allowed((self.x + self.speed, self.y), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["right"]
                self.x += self.speed

        self.update_tile_pos()

    def toggle_powerups(self):
        pass
    
    def alive(self):
        if self.hp <= 0:
            print(f"Player dead")
            return False
        return True