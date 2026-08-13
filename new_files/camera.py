import pygame as py

class Camera():
    def __init__(self, camera):
        self.camera_pos = camera

    def update_camera(self, player_center, screen, world_dim, tile_size):
        center_screen = (screen[0]//2, screen[1]//2)
        world = [x*tile_size for x in world_dim]
        target_x, target_y = 0, 0

        if player_center[0] <= center_screen[0]:
            target_x = 0

        if player_center[1] <= center_screen[1]:
            target_y = 0


        if center_screen[0] < player_center[0] <= (world[0] - center_screen[0]):
            target_x = player_center[0] - center_screen[0]

        if center_screen[1] < player_center[1] <= (world[1] - center_screen[1]):
            target_y = player_center[1] - center_screen[1]


        if (world[0] - center_screen[0]) < player_center[0] <= world[0]:
                    target_x = world[0] - screen[0]

        if (world[1] - center_screen[1]) < player_center[1] <= world[1]:
                    target_y = world[1] - screen[1]

        #print(f"this is my targetx '{target_x}' and this is my targety '{target_y}' ")
        self.camera_pos = (target_x, target_y)


    