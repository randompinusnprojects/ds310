#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# Please refer to README.md for further explanation

import pandas as pd
import sqlite3
import time



# In[ ]:


class Node:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.keys = []  # List of keys in the node
        self.values = []  # Corresponding values for leaf nodes, else left blank
        self.children = []  # List of child nodes (for internal nodes)
        self.leaf = leaf  # Boolean flag to check if the node is a leaf, for B plus trees this is necessary
        self.parent = None  # Reference to parent node
        self.next_leaf = None  # Pointer to the next leaf node for linked leaves

        # In B plus trees, internal nodes do not hold any values, instead serve as pointers for navigating the tree


# In[ ]:


class BPlusTree:
    def __init__(self, t):
        self.root = Node(t, leaf=True)  # Root starts as a leaf node
        self.t = t

    def insert(self, key, value):
        node = self.root
        if self.search(key):
          # print(f'existing key, rewriting value')
          node = self.get_node(key)
          node.values[node.keys.index(key)] = value
          return

        while not node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]: # use short-circuit
                i += 1

            if i >= len(node.children):
                i = len(node.children) - 1  # If i is out of bounds, point to the last child
            node = node.children[i]
        
        # Add your code here
        # Hints:
        # 1. Insert the key and value into the correct position in this leaf node
        # 2. Handle overflow (if number of keys exceeds 2*t, call split_child)
        # 3. If splitting root, create a new root
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
                i = node.parent.children.index(node) # just to avoid subtracting when i == len
            self.split_child(node.parent, i)
            node = node.parent
            self.sort(node)
    
        

    def split_child(self, parent, index):
        """
        Split the child node at 'index' of parent.
        For B+ trees:
          - Internal nodes only store keys (no values)
          - Leaf nodes store both keys and values
        """
        node = parent.children[index]
        t = self.t
        num_keys = len(node.keys)

        # Calculate the mid index for splitting
        mid_index = num_keys // 2

        new_node = Node(t, leaf=node.leaf)  # Create a new node to hold the split values
        new_node.keys = node.keys[mid_index:]  # Second half of keys
        new_node.values = node.values[mid_index:]  # Second half of values for leaf node
        new_node.parent = parent  # Set parent of the new node
    
        if not node.leaf:
            new_node.children = node.children[mid_index:]
            for child in new_node.children:
                child.parent = new_node
            node.children = node.children[:mid_index]

        # Keep only first half in original node
        promoted_key = node.keys[mid_index]
        node.keys = node.keys[:mid_index]
        node.values = node.values[:mid_index]
        # print(f'adding relation between {node.keys} -> {new_node.keys}')
        old_next = node.next_leaf
        new_node.next_leaf = old_next
        node.next_leaf = new_node

        # Insert promoted key and new node into parent
        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, promoted_key)

        if not new_node.leaf:
            # print(f'erasing relation {node.keys} -> {new_node.keys}')
            new_node.keys = new_node.keys[1:]
            new_node.values = new_node.values[1:]
            node.next_leaf = None
            new_node.next_leaf = None

    def sort(self, node):
        if node.leaf:
            d = {node.keys[i]: node.values[i] for i in range(len(node.keys))}
            d = {k:v for k, v in sorted(d.items(), key=lambda item: item[0])}
            node.keys = list(d.keys())
            node.values = list(d.values())
        else:
            node.keys.sort()

    def search(self, key):
        """
        :param key: The key to search for in the B+ tree.
        :return: The value associated with the key if found, or None if not found.
        """
        node = self.root
        # Add your code here
        # Hints:
        # 1. Traverse down internal nodes using keys until you reach a leaf
        # 2. Once at a leaf, check if the key exists
        # 3. Return the value if found, otherwise return None
        # print(f'searching node {node.keys} for key {key}')
        while not node.leaf and node.children:
            node = node.children[0]
        
        # print(f'traversed to node {node.keys} which is a leaf? {node.leaf}')
        while key not in node.keys and node.next_leaf:
            node = node.next_leaf
        # print(f'final destination is {node.keys}')
        if key in node.keys:
            return node.values[node.keys.index(key)] 
        return None

    def get_node(self, key):
        node = self.root
        i = 0
        while not node.leaf and node.children:
            node = node.children[0]
    
        while key not in node.keys and node.next_leaf:
            node = node.next_leaf
    
        if key in node.keys:
            return node
        return None
        

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, ":", node.keys)
        for child in node.children:
            self.print_tree(child, level + 1)

    def print_ll(self, node=None, level=0):
        if node is None:
            node = self.root
        if node.leaf and node.next_leaf:
            print("Level", level, ":", node.keys, "->", node.next_leaf.keys)
        for child in node.children:
            self.print_ll(child, level + 1)


# In[ ]:


# Example test case
# This is a very face level test to ensure your code runs, you should add more
# keys to ensure your logic is correct for more complex cases
"""
print('testcase1')
bplus_tree = BPlusTree(2)
bplus_tree.insert(15, '21')
bplus_tree.insert(25, '31')
bplus_tree.insert(35, '41')
bplus_tree.insert(45, '10')
bplus_tree.insert(5, '33')
bplus_tree.print_tree()

print('testcase2')
testplustree = BPlusTree(2)
testplustree.insert(4, 4)
testplustree.insert(9, 9)
testplustree.insert(7, 7)
testplustree.insert(14, 14)
testplustree.insert(16, 16)
testplustree.insert(20, 20)
testplustree.insert(19, 19)
testplustree.insert(27, 27)
testplustree.insert(18, 18)
testplustree.insert(13, 13)
testplustree.insert(21, 21)
testplustree.insert(25, 25)
testplustree.insert(22, 22)
testplustree.insert(24, 24)
testplustree.insert(14, 144)
testplustree.print_tree()
testplustree.print_ll()

print('test_search')
print(testplustree.search(19))
print(testplustree.search(24))
print(testplustree.search(14))
print(testplustree.search(999))
"""


print('extra test case to debug the autograder results')
please = BPlusTree(2)
please.insert(30, 30)
please.insert(31, 31)
please.insert(32, 32)
please.insert(20, 20)
please.insert(34, 34)
please.insert(33, 33)
please.insert(25, 25)
please.insert(17, 17)
please.insert(19, 19)
please.insert(12, 12)
please.insert(10, 10)
please.insert(13, 13)
please.insert(16, 16)
please.insert(7, 7)
please.insert(9, 9)
please.insert(8, 8)
please.insert(5, 5)
please.insert(6, 6)
print('\n\n')
please.print_tree()
please.print_ll()
print('\n')
please.search(10)
please.search(25)
please.search(35)
# In[ ]:





# In[ ]:




