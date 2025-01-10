import numpy as np
from tree_class import Tree, TreeNode

tree = Tree()

next_node = tree.root
open_list = [tree.root]
open_positions = []

def get_next_pos_dfs(grid, position):
    global next_node
    add_adjacent_nodes(grid, position, next_node)
    next_node = open_list.pop()
    # if reached_goal(grid, next_node.pos): print(path_to_node(next_node))
    return next_node.pos

def get_next_pos_bfs(grid, position):
    global next_node
    add_adjacent_nodes(grid, position, next_node)
    next_node = open_list.pop(0)
    # if reached_goal(grid, next_node.pos): print(path_to_node(next_node))
    return next_node.pos

def get_next_pos(grid, position):
    global next_node
    add_adjacent_nodes(grid, position, next_node)
    next_node = open_list.pop(0)
    if reached_goal(grid, next_node.pos): print(path_to_node(next_node))
    return next_node.pos

def path_to_node(node):
    path = []
    while node is not None:
        path.append((int(node.pos[0]), int(node.pos[1])))
        node = node.parent

    path.reverse()
    return path

def add_adjacent_nodes(grid, position, current_node):
    global open_list

    children_nodes = [TreeNode(current_node, pos = tuple(entry)) for entry in ( np.array([(0, 1), (0, -1), (1, 0), (-1, 0)]) + np.array(position)) 
                     if ((not (0 in tuple(entry) or -1 in tuple(entry) or grid.shape[0]-1 <= tuple(entry)[0] or grid.shape[1]-1 <= tuple(entry)[1])) 
                         and grid[tuple(entry)[0]][tuple(entry)[1]] == 0
                         and tuple(entry) not in open_positions 
                         )]
    
    current_node.children = [child for child in children_nodes if child.pos not in open_positions]
    open_positions.extend([child.pos for child in children_nodes])

    open_list.extend(children_nodes)

def reached_goal(maze, pos):
    height, width = maze.shape
    return pos == (height - 2, width - 2)

def run_maze(maze, algo="dfs"):
    global next_node, open_list, open_positions
    next_node = tree.root
    open_list = [tree.root]
    open_positions = []
    pos = (0, 1)

    if algo == "dfs":
        while not reached_goal(maze, pos):
            pos = get_next_pos_dfs(maze, pos)
    elif algo == "bfs":
        while not reached_goal(maze, pos):
            pos = get_next_pos_bfs(maze, pos)


    # print(path_to_node(next_node))