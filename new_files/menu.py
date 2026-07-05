import pygame as pg
import cte
import animation as anim

scale = 5
center_play = (13, 12) 
center_quit = (15, 18)
centerx_butt = cte.screen_w//2
y_butt_p, y_butt_q = 280, 430

def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    

class Menu():
    def __init__(self):
        self.font = pg.font.SysFont("arialblack", size = 30)
        self.text_col = (255, 255, 255)
        self.mouse_click = False
        self.start = None

        self.scaled_img_p = pg.transform.scale_by(anim.play_quit["play"], scale)
        self.rect_p = self.scaled_img_p.get_rect()
        self.scaled_img_q = pg.transform.scale_by(anim.play_quit["quit"], scale)
        self.rect_q = self.scaled_img_q.get_rect()

    def show_menu(self, protocol, screen, events, x=None, y=None):
        screen.fill((100, 100, 100))
        if protocol == "start":
            self.rect_p.midtop = (centerx_butt, y_butt_p)
            screen.blit(self.scaled_img_p, (self.rect_p))
            
            self.rect_q.midtop = (centerx_butt, y_butt_q)
            screen.blit(self.scaled_img_q, (self.rect_q))

        #########events#########
        mouse_pos = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT:
                self.start = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_click = True
                if self.rect_p.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.start = True
                if self.rect_q.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.start = False
            if event.type == pg.MOUSEBUTTONUP:
                self.mouse_click = False
        ########################

        if self.rect_p.collidepoint(mouse_pos[0], mouse_pos[1]):
            if self.mouse_click:
                self.start = True
                print(f"you are in the game!")
        
        if self.rect_q.collidepoint(mouse_pos[0], mouse_pos[1]):
            if self.mouse_click:
                self.start = False
                print(f"you exited the game!")
    
        pg.display.flip()