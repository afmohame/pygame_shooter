import pygame
import spritesheet
import power_ups

pygame.init()
#-----------------------------------------------
#                   CLASSEN
#-----------------------------------------------
class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Character(Position):
    def __init__(self, x, y, HP, defense, speed, width, height, color, sprite_sheet):
        super().__init__(x, y)
        self.HP = HP
        self.defense = defense
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color    
        self.img_sprite = sprite_sheet
    
    def extract_sprite(self):
        self.char_sprite = spritesheet.Sprites(self.img_sprite)
        #0 is the frame I want to use, width/height is  the height of the sprites box, scale is multiplier to make it bigger
        self.image = self.char_sprite.get_image(0, self.width, self.height, 3, black) 

    '''def animation(self):
        self.animation_list = []
        self.animation_steps = 5 #how many images per task
        #for loop to iterate 
        Work in progress'''

    def draw(self):
        pygame.draw.rect(screen, self.color, rect=(self.x, self.y, self.width*3, self.height*3))
        return self.image

class Player(Character):
    def __init__(self, x, y, HP, defense, speed, width, height, color, sprite_sheet, stamina, power_up = (None, None)):
        super().__init__(x, y, HP, defense, speed, width, height, color, sprite_sheet)
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
    #geen idee hoe dit implementeren
    #def toggle_powerups(self):
    #    pass

class Enemies(Character):
    def __init__(self, HP, defense, speed):
        #super().__init__(HP, defense, speed)
        pass

class Weapons():
    def __init__(self, shooting_power, drop_rate, type, image, bullet_count = None):
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.type = type
        self.bullet_count = bullet_count

#-----------------------------------------------
#                  CONSTANTE
#-----------------------------------------------
player_sprite_width, player_sprite_height = 20, 23
xpos, ypos, spd, width, height = 50, 50, 2, 40, 65
list_of_players, list_of_sprites = [], []
standing_front, standing_back, standing_side, running_front, running_back, running_side = 0, 2, 1, 3, 5, 4
dead = 9
#SCREEN
screen_w, screen_h = 1500, 900 #breedte scherm, hoogte scherm
fps = 60 
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
black = (0, 0, 0)
bg = (100, 100, 100) #background

#SPRITES
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
gun1 = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
#with or without convert_alpha it still works--> better performance?

#CHARACTERS
player = Player(xpos, ypos, 60, 10, spd, player_sprite_width, player_sprite_height, (255, 0, 0), sprite_player, 10, (None, None))
player.extract_sprite()


#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
list_of_players.append(player)
run = True
while run:
    screen.fill(bg) #can't be deleted it refreshes the screen.
    #screen.blit(frame_0, (250, 250))
    #screen.blit(frame_4, (300, 300))
    #screen.blit(sprite_player, (250, 250))#This shows the whole sprite sheet
    if player in list_of_players:
        if hasattr(player, "draw"):
            screen.blit(player.draw(), (player.x, player.y))
            screen.blit(gun1, (player.x+width, player.y+height/2.5))#puts a surface on another surface
        if hasattr(player, "moving"):
            player.moving()
        if hasattr(player, "toggle"):
            pass # player.toggle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()