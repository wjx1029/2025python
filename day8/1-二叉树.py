# Author: Sean W
# 2026年01月08日19时26分51秒
# wanjx0701@gmail.com

class Node:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree:
    def __init__(self):
        self.root = None
        self.helper_queue = []  # 辅助队列

    def level_build_tree(self, node: Node):
        if self.root is None:  # 树根为空
            self.root = node
            self.helper_queue.append(node)
        else:
            self.helper_queue.append(node)
            if self.helper_queue[0].left is None:  # 如果当前的父亲左孩子是None
                self.helper_queue[0].left = node  # 放入左孩子
            else:
                self.helper_queue[0].right = node  # 放入右孩子
                del self.helper_queue[0]  # 当前父亲满了，出队

    def pre_order(self, cur_node: Node):
        if cur_node:
            print(f'{cur_node.val}', end=' ')
            self.pre_order(cur_node.left)
            self.pre_order(cur_node.right)

    def mid_order(self, current_node: Node):
        if current_node:
            self.mid_order(current_node.left)
            print(current_node.val, end=' ')
            self.mid_order(current_node.right)

    def last_order(self, current_node: Node):
        if current_node:
            self.last_order(current_node.left)
            self.last_order(current_node.right)
            print(current_node.val, end=' ')

    def level_order(self):
        helper_queue = [self.root]
        while helper_queue:
            cur_node: Node = helper_queue.pop(0)
            print(cur_node.val, end=' ')
            if cur_node.left:
                helper_queue.append(cur_node.left)
            if cur_node.right:
                helper_queue.append(cur_node.right)


if __name__ == '__main__':
    tree = BinaryTree()
    for i in range(1, 11):
        node = Node(i)
        tree.level_build_tree(node)

    tree.pre_order(tree.root)  # 前序遍历，就是深度优先遍历
    print()
    tree.mid_order(tree.root)
    print()
    tree.last_order(tree.root)
    print()
    tree.level_order()
