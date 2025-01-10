'''
Repo available at https://github.com/Hal609/PythonSearchVisualiser
'''

from vis import run_grid_vis
from navigate_maze import run_maze
from maze_generator import create_maze

import matplotlib.pyplot as plt

import time

def make_maze(size=25):
    maze = create_maze(size, size)

    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            if cell != 1:
                maze[x][y] = 0

    return maze

run_grid_vis(make_maze(size=19))

# dfs_output = open(f"results/dfs_results_small_sample.csv", "w+")
# bfs_output = open(f"results/bfs_results_small_sample.csv", "w+")
# bfs_output.write("grid_size,average_time_ns")
# dfs_output.write("grid_size,average_time_ns")

# dfs_total_time = 0
# bfs_total_time = 0
# num_runs = 5

# ns = []
# times = []
# for n in range(9, 300, 4):
#     total_time = 0
#     for i in range(num_runs):
#         maze = make_maze(size=n)
#         dfs_start_time = time.time_ns()
#         run_maze(maze, algo="dfs")
#         dfs_total_time += time.time_ns() - dfs_start_time
#         bfs_start_time = time.time_ns()
#         run_maze(maze, algo="bfs")
#         bfs_total_time += time.time_ns() - bfs_start_time
#     dfs_output.write(f"\n{n}, {dfs_total_time/num_runs}")
#     bfs_output.write(f"\n{n}, {bfs_total_time/num_runs}")
#     print(f"\nFor a grid size of {n}:\nThe average duration for bfs was {round(bfs_total_time/num_runs / 1e6, 3)}ms\nThe average duration for dfs was {round(dfs_total_time/num_runs / 1e6, 3)}ms")

# dfs_output.close()
# bfs_output.close()
