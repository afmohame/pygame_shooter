import pygame as pg
import cte

def to_tiles(x, y):
    tile_pos = (int(x//cte.tile_size[0]), int(y//cte.tile_size[0]))
    return tile_pos