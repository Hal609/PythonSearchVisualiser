import numpy as np
import random as rn

visited = set()
frontier = []

def get_valid_adjacent(grid, position):
    visited.add(position)

    grid_width, grid_height = grid.shape
    adjacent = []
    directions = np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])
    for entry in directions + np.array(position):
        entry = tuple(entry)
        if not (0 in entry or -1 in entry or grid_width-1 <= entry[0] or grid_height-1 <= entry[1]):
            if grid[entry[0]][entry[1]] == 22:
                if entry not in frontier and entry not in visited:
                    frontier.append(entry)
                adjacent.append(entry)

    return tuple(adjacent)

full_path = []
current_branch = []
def get_next_pos(grid, position):
    global full_path
    adjacent = get_valid_adjacent(grid, position)
    next = frontier.pop()
    full_path.append(next)
    # if next in adjacent:
    # else:
    #     best_path = best_path[:-5]
    # print(full_path)
    return next