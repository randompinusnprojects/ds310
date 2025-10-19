# Plase refer to README.md for further explanation

import pandas as pd
import sqlite3
import time

class Node:
  def __init__(self, t, leaf=False):
    self.t = t
    self.keys = []
    self.values = [] # internal nodes don't hold values but serve as pointers
    self.children = []
    self.leaf = leaf
    self.parent = None
    self.next_leaf = None # for linked leaves

class BPlusTree:
  def __init__(self, t):
    self.root = Node(t, leaf=True)
    self.t = t

  def insert(self, key, value):
    node = self.root
    if self.search(key):
      # print(f"existing key, appending value")
      node = self.get_node(key) 
      node.values[node.keys.index(key)].append(value) # help
      return 
    while not node.leaf:
      i = 0
      while i < len(node.keys) and key > node.keys[i]:
        i += 1

      if i >= len(node.children):
        i = len(node.children) - 1 # if i is out of bounds point to last child
      node = node.children[i] # went to the right child and navigated to leaf ig

      """ Add code here """
    node.keys.append(key)
    node.values.append([value])
  
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
       - Internal nodes only store keys (no vals)
       - Leaf node store both keys and values
    """
    node = parent.children[index]
    t = self.t
    num_keys = len(node.keys)

    # Calculate the mid index for splitting
    mid_index = num_keys // 2

    new_node = Node(t, leaf=node.leaf) # new node to hold split vlas
    new_node.keys = node.keys[mid_index:]
    new_node.values = node.values[mid_index:]
    new_node.parent = parent

    if not node.leaf:
      new_node.children = node.children[mid_index:]
      for child in new_node.children:
        child.parent = new_node
      node.children = node.children[:mid_index]

    # keep only first half in original node
    promoted_key = node.keys[mid_index]
    node.keys = node.keys[:mid_index]
    node.values = node.values[:mid_index] # no popping needed but include
    old_next = node.next_leaf
    new_node.next_leaf = old_next
    node.next_leaf = new_node

    # insert promoted key and new node into parent
    parent.children.insert(index + 1, new_node)
    parent.keys.insert(index, promoted_key)

    if not new_node.leaf: # for internal nodes, remove the promoted key and value
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
    node = self.root
    """ 
    Add code here
    Hint:
    1. Traverse down internal nodes using keys until you reach a leaf
    2. Once at leaf, check if key exists
    3. Return the val if found, otherwise return None
    """
    while not node.leaf and node.children: # traverse to leaf
      node = node.children[0]
    
    while key not in node.keys and node.next_leaf: # traverse leaves
      node = node.next_leaf
    
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

  def print_treevals(self, node=None, level=0):
    if node is None:
      node = self.root
    print("Level", level, ":", node.values)
    for child in node.children:
      self.print_treevals(child, level + 1)

  def print_ll(self, node=None, level=0):
    if node is None:
      node = self.root
    if node.leaf and node.next_leaf:
      print("Level", level, ":", node.keys, "->", node.next_leaf.keys)
    for child in node.children:
      self.print_ll(child, level + 1)



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

