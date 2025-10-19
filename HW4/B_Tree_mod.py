# Please refer to README.md for further explanation
import pandas as pd
import sqlite3
import time

class Node:
  def __init__(self, t):
    self.t = t # Minimum degree
    self.keys = [] # list of keys
    self.values = [] # corresponding vals
    self.children = [] # list of child nodes
    self.parent = None # Ref to parent node

class BTree:
  def __init__(self, t):
    self.root = Node(t)
    self.t = t

  def insert(self, key, value):
    if self.search(key):
      # print(f"existing key, appending value")
      node = self.get_node(key)
      node.values[node.keys.index(key)].append(value) 
      return 

    node = self.root
    if not node.keys: 
      node.keys.append(key)
      node.values.append([value])
      return
      """
      Add code here
      1. Traverse down to the correct leaf node (while node.children)
      2. Insert the key in sorted order
      3. If node overflows (len(node.keys)>2*t), call split_child()
      """
    i = 0
    l = 0
    while node.children: # goal is to get into right node
      # print(f'level: {l}')
      i = 0
      while i < len(node.keys) and key > node.keys[i]:
        # print(f'comparing {node.keys[i]} and {key}')
        i += 1
      node = node.children[i]
      l += 1
      
    node.keys.append(key)
    node.values.append([value])
    
    self.sort(node)

    while len(node.keys)>2*self.t:
      # print(f'overflowed in {node.keys}')
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
        

  def sort(self, node):
    d = {node.keys[i]: node.values[i] for i in range(len(node.keys))}
    d = {k:v for k, v in sorted(d.items(), key=lambda item: item[0])}
    node.keys = list(d.keys())
    node.values = list(d.values())

  def split_child(self, parent, index):
    # print(f'working with parent {parent.keys} with index {index}')
    node = parent.children[index]
    t = self.t # min degree
    num_keys = len(node.keys)

    mid_index = t + 1 

    new_node = Node(t)
    new_node.keys = node.keys[mid_index:]
    new_node.values = node.values[mid_index:]
    new_node.parent = parent

    if node.children:
      for n in node.children[int(len(node.children)/2):]:
        n.parent = new_node
        new_node.children.append(n)
        node.children.pop(-1)

    node.keys = node.keys[:mid_index]
    node.values = node.values[:mid_index]

    # insert new node into parent's children list
    parent.children.insert(index + 1, new_node) # insert new now after current idx
    parent.keys.insert(index, node.keys.pop(-1)) # move median key up
    parent.values.insert(index, node.values.pop(-1)) # move median val up

    # print(f'parent: {parent.keys}') 
    # print(f'node: {node.keys}') 
    # print(f'new_node: {new_node.keys}') 

  def search(self, key):
    node = self.root
    """
    Add code here
    1. Traverse node'skeys until find right spot
    2. If the key matches, return val
    3. If node has children, move down
    4. If no children and not found, return None
    """
    
    i = 0
    while key not in node.keys and node.children: # goal is to get into right node
      i = 0
      while i + 1 < len(node.keys) and key > node.keys[i]:
        # print(f'comparing {node.keys[i]} and {key}')
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
      self.print_treeval(child, level + 1)
