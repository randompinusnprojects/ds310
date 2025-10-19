# Please refer to README.md for further explanation
import pandas as pd
import sqlite3
import time

class Node:
    def __init__(self, t):
        self.t = t  # Minimum degree
        self.keys = []  # List of keys in the node
        self.values = []  # Corresponding values
        self.children = []  # List of child nodes
        self.parent = None  # Reference to parent node

class BTree:
    def __init__(self, t):
        self.root = Node(t)
        self.t = t

    def insert(self, key, value):
        node = self.root
        if self.search(key):
            # print(f'existing key, rewriting value')
            node = self.get_node(key)
            node.values[node.keys.index(key)] = value
            return
        if not node.keys:
            node.keys.append(key)
            node.values.append(value)
            return
        # Add your code here
        # Hints:
        # 1. Traverse down to the correct leaf node (use while node.children)
        # 2. Insert the key in sorted order
        # 3. If the node overflows (len(node.keys) > 2*t), call split_child()
        i = 0
        while node.children: # goal is to get into right node
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
      
        node.keys.append(key)
        node.values.append(value)
    
        self.sort(node)

        while len(node.keys)>2*self.t:
            if not node.parent:
                new_node = Node(self.t)
                node.parent = new_node
                new_node.children.append(node)
                self.root = new_node
                i = 0
            else:
                i = node.parent.children.index(node) # didn't want to subtract if i == len
            self.split_child(node.parent, i)
            node = node.parent
            self.sort(node)

    # This is a helper function designed to sort the elements in the node based on its key
    def sort(self, node):
        d = {node.keys[i]: node.values[i] for i in range(len(node.keys))}
        d = {k:v for k, v in sorted(d.items(), key=lambda item: item[0])}
        node.keys = list(d.keys())
        node.values = list(d.values())

    # This is a helper function designed to help when needing to split children of the tree
    # This should be used in your insert function
    def split_child(self, parent, index):
        """
        :param key: The parent node and index.
        :No return value:, helper function designed to aid in creating the tree.
        """
        node = parent.children[index]
        t = self.t  # Minimum degree
        num_keys = len(node.keys)

        # Determine the index to split the node
        mid_index = t+1 

        new_node = Node(t)
        new_node.keys = node.keys[mid_index:]
        new_node.values = node.values[mid_index:]
        new_node.parent = parent

        # Added case if the node also has children,
        if node.children:
            # Add your code here
            # Think about how to split children here
            # Hint: split children between node and new_node
            for n in node.children[int(len(node.children)/2):]:
                n.parent = new_node
                new_node.children.append(n)
                node.children.pop(-1)


        # Retain the first half of keys and values in the original node
        node.keys = node.keys[:mid_index]
        node.values = node.values[:mid_index]

        # Insert the new node into the parent's children list
        parent.children.insert(index + 1, new_node)  # Insert new node after current index
        parent.keys.insert(index, node.keys.pop(-1))  # Move the median key up
        parent.values.insert(index, node.values.pop(-1))  # Move the median value up

    def search(self, key):
        """
        :param key: The key to search for in the B-tree.
        :return: The value associated with the key if found, or None if not found.
        """
        node = self.root
        # Add your code here 
        # Hints
        # 1. Traverse the node's keys until you find the right spot.
        # 2. If the key matches, return the value.
        # 3. If the node has children, move down.
        # 4. If no children and not found, return None.

        i = 0
        while key not in node.keys and node.children: # goal is to get into right node
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
      
        if key in node.keys:
            return node.values[node.keys.index(key)]
        return None

    def get_node(self, key):
        node = self.root
        i = 0
        while key not in node.keys and node.children: # goal is to get into right node
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
    
        if key in node.keys: 
            return node
        return None


    # Function used to print your results, do not edit
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, ":", node.keys)
        for child in node.children:
            self.print_tree(child, level + 1)

# Example test case
# This is a very face level test to ensure your code runs, you should add more
# keys to ensure your logic is correct for more complex cases
"""
print('testcase1')
btree = BTree(2)
btree.insert(10, 'a')
btree.insert(20, 'b')
btree.insert(5, 'c')
btree.insert(6, 'd')
btree.insert(12, 'e')
btree.print_tree()

print('testcase2')
testree = BTree(2)
testree.insert(4, 4)
testree.insert(9, 9)
testree.insert(7, 7)
testree.insert(14, 14)
testree.insert(16, 16)
testree.insert(20, 20)
testree.insert(19, 19)
testree.insert(27, 27)
testree.insert(18, 18)
testree.insert(13, 13)
testree.insert(21, 21)
testree.insert(25, 25)
testree.insert(22, 22)
testree.insert(28, 28)
testree.insert(24, 24)
testree.insert(17, 17)
testree.insert(30, 30)
testree.insert(14, 144)
testree.print_tree()

print('test search')
print(testree.search(30))
print(testree.search(16))
print(testree.search(14))
print(testree.search(999))
"""
