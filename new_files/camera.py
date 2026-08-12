import pygame as py

class Camera():
    def __init__(self, camera):
        self.camera_pos = camera

    def update_camera(self, player_center, screen, world_dim, tile_size):
        target_x, target_y = player_center[0]//2, player_center[1]//2
        self.camera_pos = (target_x, target_y)

    