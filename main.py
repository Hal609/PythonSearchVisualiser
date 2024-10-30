from vis import run_grid
from create_maze import Grid, Size

grid = Grid(Size(20, 20))

from maze_generator import create_maze

maze = create_maze(21, 21)
for x, row in enumerate(maze):
    for y, cell in enumerate(row):
        if cell != 1:
            maze[x][y] = 22

run_grid(maze)