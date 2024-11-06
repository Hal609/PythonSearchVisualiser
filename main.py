from vis import run_grid
from maze_generator import create_maze

maze = create_maze(25, 25)

for x, row in enumerate(maze):
    for y, cell in enumerate(row):
        if cell != 1:
            maze[x][y] = 0

run_grid(maze)