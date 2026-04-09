import pygame

pygame.init()

#-----------------------------------------------
#                  CONSTANTE
#-----------------------------------------------
screen_w = 800 #breedte scherm
screen_h = 800 #hoogte scherm
player = pygame.Rect((300, 200, 50, 50)) #test player
fps = 30 
#-----------------------------------------------
#                   CLASSEN
#-----------------------------------------------
class Position():
    def __init__(self, x, y):
        pass

class Power_ups():
    def __init__(self, duration):
        pass

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

class Character():
    def __init__(self, HP, defense, speed, position):
        pass

class Player(Character):
    def __init__(self, HP, defense, speed, position, power_up = (None, None)):
        super().__init__(HP, defense, speed, position)
        pass

class Enemies(Character):
    def __init__(self, HP, defense, speed):
        super().__init__(HP, defense, speed)
        pass

class Weapons():
    def __init__(self, shooting_power, drop_rate, type, bullet_count = None):
        pass

#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
run = True
while run:
    screen.fill((0, 0, 0)) #kan weggelaten worden dit zorgt enkel dat window zwart is

    pygame.draw.rect(screen, (255, 0, 0), player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()