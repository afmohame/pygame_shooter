import pygame

pygame.init()

#-----------------------------------------------
#                   CLASSEN
#-----------------------------------------------
class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_image(sheet, width, height):
    pass

class Sprites(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Power_ups():
    def __init__(self, duration, drop_rate):
        self.duration = duration
        self.drop_rate = drop_rate

class Shield(Power_ups): #misschien HP i.p.v duration
    def __init__(self, duration):
        super().__init__(duration)

class Speed_boost(Power_ups):
    def __init__(self, duration, multiplier):
        super().__init__(duration)

class Rapid_fire(Power_ups):
    def __init__(self, duration, multiplier):
        super().__init__(duration)

class Health_regain(Power_ups):
    def __init__(self, duration, regain_HP):
        super().__init__(duration)

class Character(Position):
    def __init__(self, x, y, HP, defense, speed, width, height, color):
        super().__init__(x, y)
        self.HP = HP
        self.defense = defense
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color    

    def draw(self):
        pygame.draw.rect(screen, self.color, rect=(self.x, self.y, self.width, self.height))

class Player(Character):
    def __init__(self, x, y, HP, defense, speed, width, height, color, stamina, power_up = (None, None)):
        super().__init__(x, y, HP, defense, speed, width, height, color)
        self.stamina = stamina
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]

    def moving(self, vx, vy):
        self.vx, self.vy = vx, vy
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= vy
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += vy
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= vx
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += vx
    #geen idee hoe dit implementeren
    #def toggle_powerups(self):
    #    pass

class Enemies(Character):
    def __init__(self, HP, defense, speed):
        super().__init__(HP, defense, speed)
        pass

class Weapons(Player):
    def __init__(self, shooting_power, drop_rate, type, image, bullet_count = None):
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.type = type
        self.bullet_count = bullet_count

#-----------------------------------------------
#                  CONSTANTE
#-----------------------------------------------
#SCREEN
screen_w = 1500 #breedte scherm
screen_h = 900 #hoogte scherm
fps = 30 
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

#CHARACTERS
list_of_players, list_of_sprites = [], []
xpos, ypos, spd, width, height = 50, 50, 2, 40, 65
player = Player(x=xpos, y=ypos, HP=60, defense=10, speed=spd, width=width, height=height, color=(255, 0, 0), stamina=10, power_up=(None, None))
speedx, speedy = 2, 2
gun1 = pygame.image.load("sprites/images/enemy1_gun.png").convert_alpha() #with or without convert_alpha it still works--> better performance?
player_sprite = pygame.image.load().convert_alpha()
#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
list_of_players.append(player)
run = True
while run:
    screen.fill((100, 100, 100)) #can't be deleted it refreshes the screen.
    screen.blit(gun1, (player.x+width, player.y+height/2.5))#puts a surface on another surface
    if player in list_of_players:
        if hasattr(player, "draw"):
            player.draw()
        if hasattr(player, "moving"):
            player.moving(speedx, speedy)
        if hasattr(player, "toggle"):
            pass # player.toggle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()