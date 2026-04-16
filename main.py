import pygame
import spritesheet
import power_ups

pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
class Character():
    def __init__(self, x, y, hp, defense, speed, hitbox_width, hitbox_height, hitbox_color, sprite_sheet):
        self.x, self.y = x, y
        self.hp = hp
        self.defense = defense
        self.speed = speed
        self.hitbox_width = hitbox_width 
        self.hitbox_height = hitbox_height 
        self.hitbox_color = hitbox_color  #temporary
        self.sprite_sheet = spritesheet.Sprites(sprite_sheet)
    
    def make_sprite(self, transparancy_color, scale, frame_index, column_index, first_x, first_y, x_space, y_space):
        self.scale = scale
        #0 is the frame I want to use, width/height is  the height of the sprites box, scale is multiplier to make it bigger
        self.image = self.sprite_sheet.slice_sheet(frame_index, column_index, first_x, first_y, self.hitbox_width, self.hitbox_height, scale, 
                                                   transparancy_color, x_space, y_space)

    def get_sprite(self):
        return self.image
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.hitbox_color, rect=(self.x, self.y, (self.hitbox_width)*self.scale, 
                                                           (self.hitbox_height)*self.scale))
        

class Player(Character):
    def __init__(self, x, y, hp, defense, speed, hitbox_width, hitbox_height, hitbox_color, sprite_sheet, stamina, power_up = (None, None)):
        super().__init__(x, y, hp, defense, speed, hitbox_width, hitbox_height, hitbox_color, sprite_sheet)
        self.stamina = stamina
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]
    
    
    def moving(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
    """geen idee hoe dit implementeren
    #def toggle_powerups(self):
        pass"""

class Enemies(Character):
    def __init__(self, hp, defense, speed):
        #super().__init__(hp, defense, speed)
        pass

class Weapons():
    def __init__(self, shooting_power, drop_rate, kind, image, bullet_count = None):
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.kind = kind
        self.image = image
        self.bullet_count = bullet_count
    
    def moving_with_cursor(self):
        pass

#-----------------------------------------------
#                  constants
#-----------------------------------------------
# screen
screen_w = 1500
screen_h = 900
fps = 60
black = (0, 0, 0)
bg = (100, 100, 100)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_w, screen_h))

# player
player_sprite_width = 14
player_sprite_height = 21
xpos = 0
ypos = 0
hp = 30
defense = 10
spd = 2
hitbox_width = 40
hitbox_height = 65
hitbox_color = (255, 0, 0)
stamina = 10
# animation frames
standing_front = 0
standing_side = 1
standing_back = 2
running_front = 3
running_side = 4
running_back = 5
dead = 9

# sprite state
frame_index = 0
column_index = 0
first_x, x_space = 2, 48
first_y, y_space = 0, 48
scale = 2.5
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
gun1 = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 


#OTHERS
list_of_players, list_of_guns = [], []
player = Player(
    xpos, ypos, hp, defense, spd,
    player_sprite_width, player_sprite_height,
    hitbox_color, sprite_player, stamina, (None, None)
)

weapon_x = player_sprite_width+15
weapon_y = player_sprite_height+5

#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------

player.make_sprite(black, scale, frame_index, column_index, first_x, first_y, x_space, y_space)
list_of_players.append(player)
run = True
while run:
    screen.fill(bg) #can't be deleted it refreshes the screen.
    for character in list_of_players:
        character.draw(screen)
        #puts a surface on another surface
        screen.blit(gun1, (character.x + weapon_x, character.y + weapon_y))
        screen.blit(character.get_sprite(), (character.x, character.y))
        character.moving()
        # player.toggle()
        #the ifs are not needed don't know why we should use them
        """
        if hasattr(character, "draw"):
            character.draw(screen)
            #puts a surface on another surface
            screen.blit(gun1, (character.x + weapon_x, character.y + weapon_y))
        if hasattr(character, "get_sprite"):
            screen.blit(character.get_sprite(), (character.x, character.y))
        if hasattr(character, "moving"):
            character.moving()
        if hasattr(character, "toggle"):
            pass # player.toggle()"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()