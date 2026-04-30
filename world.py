import pygame as pg
import numpy

world_width, world_height = 20, 10
tile_size = 30
#numpy.zeros((rows, columns)) or numpy.zeros((height, width))
world_map = numpy.zeros((world_height, world_width), dtype = int)
gift_map = numpy.zeros((world_height, world_width), dtype = int)
world_map[0, :] = 2 #first row to last column --> top row
world_map[-1, :] = 2 #last row to last column --> bottom row
world_map[:, 0] = 2 #first column to last row --> left row
world_map[:, -1] = 2 #last column to last row --> right row


print(world_map)




"""
0 is walkable
1 destructable wall but not walkable if wall there
    --> 0 nothing = 92%
    --> 1 is random gun 5% 
    --> 2 is power_up 3%
2 non destructible oute walls bullets can ricochet on them
"""