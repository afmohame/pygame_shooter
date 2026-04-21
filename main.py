import pygame
import spritesheet
import power_ups

pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y

class Character(Position):
    def __init__(self, x, y, hp, defense, speed, hitbox_width, hitbox_height, sprite_player_width, sprite_player_height, hitbox_color, sprite_sheet, 
                 scale, animation_steps, column_index):
        super().__init__(x, y)
        self.hp = hp
        self.defense = defense
        self.speed = speed
        self.sprite_player_width = sprite_player_width 
        self.sprite_player_height = sprite_player_height
        self.hitbox_width = hitbox_width
        self.hitbox_height = hitbox_height 
        self.hitbox_color = hitbox_color  #temporary
        self.sprite_sheet = spritesheet.Sprites(sprite_sheet)
        self.scale = scale
        self.animation_steps = animation_steps
        self.column_index = column_index
        self.animation_seq = []
            
    def make_animation(self, transparancy_color, first_x, first_y, x_space, y_space, column_length):
        #0 is the frame I want to use, width/height is  the height of the sprites box, scale is multiplier to make it bigger
        self.animation_seq = self.sprite_sheet.animation(self.animation_steps, self.column_index, first_x, first_y, self.sprite_player_width, 
                                                         self.sprite_player_height, self.scale, transparancy_color, x_space, y_space, column_length)
    def get_animation(self, frame):
        self.length_animation_list = len(self.animation_seq) 
        return self.animation_seq[frame]
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.hitbox_color, rect=(self.x, self.y, (self.hitbox_width)*self.scale, 
                                                           (self.hitbox_height)*self.scale))
        
class Player(Character):
    def __init__(self, x, y, hp, defense, speed, hitbox_width, hitbox_height, sprite_player_width, sprite_player_height, hitbox_color, sprite_sheet, 
                 scale, frame_index, column_index, stamina, power_up = (None, None)):
        super().__init__(x, y, hp, defense, speed, hitbox_width, hitbox_height, sprite_player_width, sprite_player_height, hitbox_color, sprite_sheet, scale,
                        frame_index, column_index)
        self.stamina = stamina
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]
    
    #need to find a way to put it in character class 
    def moving(self, running_up, running_down, running_right, running_left):
        keys = pygame.key.get_pressed()
        self.column_index = 0 #column index for resting sprite
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.column_index = running_up
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.column_index = running_down
            self.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.column_index = running_left
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.column_index = running_right
            self.x += self.speed

    def toggle_powerups(self):
        pass

class Enemies(Character):
    def __init__(self, hp, defense, speed):
        #super().__init__(hp, defense, speed)
        pass

class Weapons(Position):
    def __init__(self, x, y, shooting_power, drop_rate, rarity, image, radius, ricochet, center_char, bullet_count = None):
        super().__init__(x, y)
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.rarity = rarity
        self.image = image
        self.radius = radius
        self.ricochet = ricochet
        self.center_char = center_char #tuple (x, y)
        self.bullet_count = bullet_count
    
    def Rotate_gun(self, mx, my, angle):
        self.mx = mx
        self.my = my
        self.angle = angle

    def Shoot(self, shoot):
        if shoot:
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

# animation frames
standing_front = 0
standing_side = 1
standing_back = 2
running_down = 3
running_right, running_left = 4, -4#-4 so it can be identified and mirrored in slice_sheet method inside Sprites class
running_up = 5
dead = 9
column_index = 0
first_x, x_space = 2, 48
first_y, y_space = 0, 48
scale = 3
column_length = 255

# sprite state
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
last_update = pygame.time.get_ticks()
animation_cooldown = 100 #miliseconds
frame = 0 

#create animation list
animation_list = []
animation_steps = 6 #there are 6 sprites for each animation

# player
sprite_player_width = 14
sprite_player_height = 21
xpos = 0
ypos = 0
hp = 30
defense = 10
spd = 5
hitbox_width = 40 
hitbox_height = 65
hitbox_color = (255, 0, 0)
stamina = scale
player = Player(
    xpos, ypos, hp, defense, spd, hitbox_width, hitbox_height,
    sprite_player_width, sprite_player_height,
    hitbox_color, sprite_player, scale, animation_steps,
    column_index, stamina, (None, None)
)

#guns
center_charx, center_chary = sprite_player_width/2, sprite_player_height/2
radius = sprite_player_height/2
weapon_x = sprite_player_width*scale
weapon_y = scale*sprite_player_height/2
revolver = Weapons(weapon_x, weapon_y, 3, 10, "common", sprite_revolver, radius, 2, (center_charx, center_chary))

#OTHERS
list_of_players, list_of_enemies, list_of_guns = [], [], []


#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
list_of_players.append(player)
list_of_guns.append(revolver)
run = True
while run:
    screen.fill(bg) #can't be deleted it refreshes the screen.

    #this block needs to be above other event.type otherwise it does not work 
    #repeating for event in pygame.event.get() is also not good
    #for loop does not create a local variable!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update animation
    current_time = pygame.time.get_ticks()#for animation tracks time passed
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= 6:#len(animation_list):
            frame = 0

    for character in list_of_players:
        #character.draw(screen)#draws a hitbox in red
        character.moving(running_up, running_down, running_right, running_left)
        character.make_animation(black, first_x, first_y, x_space, y_space, column_length)
        screen.blit(character.get_animation(frame), (character.x, character.y))#puts character on screen which is a surface
    for gun in list_of_guns:
            screen.blit(gun.image, (character.x + weapon_x, character.y + weapon_y))#puts gun on screen which is a surface
        

    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        gun.x = pos[0]
        gun.y = pos[1]
        print(gun.x)
    if event.type == pygame.MOUSEBUTTONUP:
        pass        
    if event.type == pygame.MOUSEBUTTONDOWN:
        pass  


    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()