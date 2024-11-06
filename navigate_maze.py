import numpy as np
from tree_class import Tree, TreeNode

tree = Tree()

open_list = []
open_positions = []
next_node = tree.root

def get_next_pos(grid, position):
    global next_node, first_run
    add_adjacent_nodes(grid, position, next_node)
    next_node = open_list.pop()
    print(tree)
    
    return next_node.pos

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