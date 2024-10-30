import random
import numpy as np

class Size: 
    def __init__(self, height, width): 
        self.height = height
        self.width = width
        self.tuple = (height, width)

class Grid():
    def __init__(self, size = Size(10, 10)):
        self.size = size
        self.shape = (size.width, size.height)
        self.start_wall = random.choice(["left", "right", "top", "bottom"])
        self.start_wall_coords = self.get_wall_coords()
        self.start = self.pick_start()
        self.grid = self.init_grid()

    def get_numpy_grid(self):
        return self.grid

    def get_wall_coords(self):
        coords = []
        if self.start_wall == "left":
            for y in range(self.size.height):
                coords.append((y, 0))
        if self.start_wall == "right":
            for y in range(self.size.height):
                coords.append((y, self.size.width - 1))
        if self.start_wall == "top":
            for x in range(self.size.width):
                coords.append((0, x))
        if self.start_wall == "bottom":
            for x in range(self.size.width):
                coords.append((self.size.height - 1, x))
        return coords

    def init_grid(self):
        grid = np.zeros(self.size.tuple)
        grid = self.add_grid_border(grid)
        grid[*self.start] = 1
        grid = self.walk_to_goal(grid)

        return grid

    def get_valid_adjacent(self, position):
        adjacent = []
        directions = np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])
        for entry in directions + np.array(position):
            entry = tuple(entry)
            if not (0 in entry or -1 in entry or self.size.width-1 <= entry[1] or self.size.height-1 <= entry[0]):
                adjacent.append(entry)
        return tuple(adjacent)

    def walk_to_goal(self, grid):
        def rank_steps(pos_list, visited):
            dist_dict = {}
            for pos in pos_list:
                if pos not in visited:
                    dist_dict[pos] = abs(pos[0] - self.start[0]) + abs(pos[1] - self.start[1])
                else:
                    dist_dict[pos] = 0
            
            best_val = 0
            best_val_keys = []
            for key in dist_dict.keys():
                if dist_dict[key] > best_val:
                    best_val = dist_dict[key]
                    best_val_keys = [key]
                elif dist_dict[key] == best_val:
                    best_val_keys.append(key)

            return random.choice(best_val_keys)

        current_pos = self.start
        visited = set(current_pos)
        for i in range(30):
            next_steps = []
            for entry in self.get_valid_adjacent(current_pos):
                if entry not in self.start_wall_coords:
                    next_steps.append(entry)

            next_pos = rank_steps(next_steps, visited)
            grid[*next_pos] = 1
            current_pos = next_pos
            visited.add(current_pos)
            if (1 in current_pos or len(grid) - 2 in current_pos or len(grid[0]) - 2 in current_pos) and len(visited) > 8:
                return grid

        return grid


    def add_grid_border(self, grid):
        for y, row in enumerate(grid):
            for x, _ in enumerate(row):
                if x == 0 or y == 0 or x == len(row) - 1 or y == len(grid) - 1:
                    grid[y][x] = 2
        return grid

    def pick_start(self):
        x_max = self.size.width - 1
        y_max = self.size.height - 1

        x_pick = random.randint(1, x_max - 1)
        y_pick = random.randint(1, y_max - 1)

        match self.start_wall:
            case "left":
                return (y_pick, 0)
            case "right":
                return (y_pick, x_max)
            case "top":
                return (0, x_pick)
            case "bottom":
                return (y_max, x_pick)
            
# size = Size(12, 12)

# init_grid(size)

if __name__ == "__main__":
    grid = Grid(Size(12, 15))
    print(grid.get_numpy_grid())
