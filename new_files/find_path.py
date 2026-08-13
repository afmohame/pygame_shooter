import pygame as pg
from queue import PriorityQueue as pq
import convert_to_tiles as ctt

class Find_path():
    def __init__(self, world):
        self.world = world

    def walkable_neighbors(self, obj_position):
        neighbors_list = []
        neighbors = {
            "up": (obj_position[0], obj_position[1] - 1),
            "right": (obj_position[0] + 1, obj_position[1]),
            "down": (obj_position[0], obj_position[1] + 1),
            "left": (obj_position[0] - 1, obj_position[1])
        }

        for key, value in neighbors.items():
            x, y = value

            if 0 <= x < self.world.world_dim[0] and 0 <= y < self.world.world_dim[1]:
                if self.world.world_map[y, x] in range(0, 2):
                    neighbors_list.append(value)

        return neighbors_list

    def find_it(self, obj_position, target_pos):
        victory_road = []
        start_tile = ctt.to_tiles(obj_position[0], obj_position[1])
        target_tile = ctt.to_tiles(target_pos[0], target_pos[1])
        checked = set()
        open_set = pq()

        g = {start_tile: 0} #tile movement adds 1
        h = abs(start_tile[0] - target_tile[0]) + abs(start_tile[1] - target_tile[1])
        t = g[start_tile] + h
        parent = {start_tile: None}

        open_set.put((t, start_tile))

        goal = False
        while not open_set.empty():
            current_record = open_set.get()
            current_t, current_tile = current_record[0], current_record[1]

            if current_tile == target_tile:
                goal = True
                break

            if current_tile not in checked:
                checked.add(current_tile)
                next_check = self.walkable_neighbors(current_tile)

                for tile in next_check:
                    if tile not in checked:
                        g_next = g[current_tile] + 1
                        h_next = abs(tile[0] - target_tile[0]) + abs(tile[1] - target_tile[1])
                        t_next = h_next + g_next

                        if tile not in g.keys() or g_next < g[tile]:
                            g[tile] = g_next
                            parent[tile] = current_tile
                            open_set.put((t_next, tile)) 


        if goal:
            current = target_tile
            while current is not None:
                victory_road.append(current)
                current = parent[current]

        if not goal:
            pass

        victory_road.reverse()
        return victory_road

                


        
    