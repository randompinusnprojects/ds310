# Hi I thought I would make a separate README file to explain my code and talk about why I have two files for each trees.

# __Summary__
    - I have two B\_Tree, BPlus\_Tree implementations that differ in handling insertions of existing keys with different values
    - Df\_Test.py uses the mod(modified) files for errorless implementation
    - methods _get_node()_, _print_treevals()_, _BPlusTree.llclean()_, _BPlusTree.print_ll()_, _BPlusTree.sort()_ have been added
    - method _BPlusTree.split_children()_ has been modified at the end for handling __internal node__ splitting (so that it doesn't retain the key being sent to parent)
    - This readme file has pseudocode for modified methods and explains differences made

# __Files in the folder__

    - __B_Tree.py__:            creates and manages btree, if you try inserting an existing key, would rewrite the original value into new value.
    - __BPlus_Tree.py__:        creates and manages btree, if you try inserting an existing key, would rewrite the original value into new value.
    - __B_Tree_mod.py__:        creates and manages bplus\_tree, if you try inserting an existing key, would append the new value to a list of original value(s).
    - __BPlus_Tree_mod.py__:    creates and manages bplus\_tree, if you try inserting an existing key, would append the new value to a list of original value(s).
    - __Df_Test.py__:           insert sql data and test (code not modified)

# __Files in detail__

## B\_Tree.py
### class
    - Node # stores k\_i in keys[i], v\_i in values[i] where v\_i is singular value
    - BTree
### main function(s) w modifications
    - insert(self, key, value)
      """
      PSEUDOCODE:
      # start from root
      if key in tree:
        # node = get\_node(key)
        # rewrite value to new value
      if no node: make new node -> exit
      while: # traverse into correct node
      append key, value in node
      sort(node)
      while overflow: 
        if no parent: # create parent node and set index to 0         
        split.\_child(node.parent, index-of-node)
        # traverse upwards and repeat until there's no overflow
      """
    - split\_child(self, parent, index)
      """
      PSEUDOCODE:
      # find node from parent
      mid\_index = t+1
      # copy second half of node into new\_node, connect w parent
      if node has children: # connect half of node.children to new\_node, pop from node.children
      # retain first half of node including mid\_key
      # insert mid\_key to parent and pop from node
      """
### helper function(s) w modifications
    - search(self, key)
      """
      PSEUDOCODE:
      # start from root
      while: # traverse into correct node
      if key in node.keys: return value
      """
    - get\_node(self, key) # the whole reason for this is to not modify search()
      """
      PSEUDOCODE:
      # start from root
      while: # traverse to right node
      if key in node: # return node
      """
### test cases
    - __testcase1__     is given testcase
    - __testcase2__     inserts keys of (#, #), except for (14, 144) to check for duplicates
    - __test_search__   tests search function with 30 (expected 30), 16 (expected 16), 14 (expected 144), 999 (expected None)

## B\_Tree\_mod.py # only inlcuded differences from B\_Tree.py
### class
    - Node # stores k\_i in keys[i], v\_i in values[i] where v\_i is list of values
    - BTree
### main function(s) w modifications
    - insert(self, key, value)
      """
      PSEUDOCODE:
      if key in tree:
        # node = get\_node(key)
        # append value to list of values corresponding to that key
      # same with B\_Tree.py
      """
### helper functions(s) w modifications
    - print\_treevals(self, node=None, level=0) # prints values of trees with same logic of print\_tree()
    
## BPlus\_Tree.py
### class
    - Node # stores k\_i in keys[i], v\_i in values[i] where v\_i is singular value
    - BPlusTree
### main function(s) w modifications
    - insert(self, key, value)
      """
      PSEUDOCODE:
      if key in tree:
        # node = get\_node(key)
        # rewrite value to new value
      while node is not leaf:
        # traverse to right leaf
      # append key and values
      while overflow: 
        if no parent: # create parent node and set index to 0         
        split.\_child(node.parent, index-of-node)
        # traverse upwards and repeat until there's no overflow
      """
    - split\_child(self, parent, index)
      """
      PSEUDOCODE:
      # same as given
      # node.next\_leaf = new\_node
      if new\_node is internal node:
        # truncate promoted key and corresponding value from new\_node
        # remove next\_leaf of node and new\_node
      """
### helper function(s) w modifications
    - sort(self, node)
      """
      PSEUDOCODE:
      if node is leaf:
        # same as BTree.sort()
      else: # sort keys only
      """
    - search(self, key)
      """
      PSEUDOCODE:
      while: # traverse down to leaf
      while: # find node with key or go to next node
      if key in node: return value
      """
    - get\_node(self, key) # the whole reason for this is to not modify search()
      """
      PSEUDOCODE:
      # start from root
      while: # traverse to right node
      if key in node: # return node
      """
    - print\_ll(self, node=None, level=0) # prints node.keys -> node.next\_leaf with same logic of print\_tree()
    
### test cases
    - __testcase1__     is given testcase
    - __testcase2__     inserts keys of (#, #), except for (14, 144) to check for duplicates
                        also check if leaves are linked well
    - __test_search__   tests search function with 19 (expected 19), 24 (expected 24), 14 (expected 144), 999 (expected None)

## BPlus\_Tree\_mod.py # only inlcuded differences from BPlus\_Tree.py
### class
    - Node # stores k\_i in keys[i], v\_i in values[i] where v\_i is list of values
    - BPlusTree
### main function(s) w modifications
    - insert(self, key, value):
      """
      PSEUDOCODE
      if key in tree:
        # node = get\_node(key)
        # append value to list of values corresponding to that key
      # same with BPlus\_Tree.py
      """
### helper function(s) w modifications
    - print\_treevals(self, node=None, level=0) # prints values of trees with same logic of print\_tree()
    

## Df\_Test.py
    - stored (k, v) as (_actor_id_, [_movie_id(s)_]) as _actor_id_ and _movie_id_ is in one to many relationship
    - for more accurate results, using mod(modified) versions of BTree and BPlusTree to handle one to many relationship is better
    - however due to autograder issues, I reverted it back to using BTree and BPlusTree

# THANKS FOR READING THIS HUMONGOUS FILE I APOLOGIZE FOR ANY INCONVENIENCE
