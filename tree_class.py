import random as rn

class TreeNode():
    def __init__(self, parent, pos: tuple, children = []) -> None:
        self.parent: TreeNode = parent
        self.pos = pos
        self.children = children
        self.visited = False

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    # def create_child(self, pos):
    #     new_child =  TreeNode(self,pos, [])
    #     self.children.append(new_child)
    #     return new_child

    def __str__(self, prefix='', is_tail=True):
        '''
        https://chatgpt.com/share/672b2844-8b58-800e-a063-2f483f16694b
        '''
        ret = prefix + ('└── ' if is_tail else '├── ') + str(self.pos) + '\n'
        for i, child in enumerate(self.children):
            is_last = i == (len(self.children) - 1)
            new_prefix = prefix + ('    ' if is_tail else '│   ')
            ret += child.__str__(new_prefix, is_last)
        return ret


class Tree():
    def __init__(self):
        self.root = TreeNode(None, (2, 1), [])

    def __str__(self):
        return self.root.__str__()

    def traverse_tree(self):
        open = []
        closed = set()
        open.append(self.root)
        while len(open) > 0:
            current_node = open.pop()
            # print("node pos:", current_node.pos)
            closed.add(current_node)

            for child in current_node.children:
                # print("child pos:", child.pos)
                open.append(child)
