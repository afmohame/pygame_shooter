import pygame as pg
import cte

def to_tiles(x, y):
    tile_pos = (int(x//cte.tile_size[0]), int(y//cte.tile_size[0]))
    return tile_pos

def to_cartesian(tile_x, tile_y):
    xy = (tile_x*cte.tile_size[0], tile_y*cte.tile_size[0])
    return xy