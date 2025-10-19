#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Please Refer to README.md for further explanation

import sqlite3
import pandas as pd
import time
from B_Tree import BTree  
from BPlus_Tree import BPlusTree 


# In[ ]:


# Load data from SQLite database
def load_data_from_db(db_path, table_name):
    """Load data from an SQLite database into a pandas DataFrame."""
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# In[ ]:


# Load Data from Movie Database (Should be in the same folder)
db_path = 'movie.sqlite'  
table_name = 'Actor'  
data = load_data_from_db(db_path, table_name)


# In[ ]:


# Create and time the B-tree insertion
btree = BTree(5)  # Initialize a B-tree with minimum degree 5
start_time = time.perf_counter()  # Start timer for B-tree insertion

# TODO: Insert each row into the B-tree
for _, (k, v) in data.iterrows():
    btree.insert(k, v)

end_time = time.perf_counter()  # End timer for B-tree insertion

# TODO: Calculate elapsed time for B-tree
btree_time = end_time - start_time

# In[ ]:


# Create and time the B+ tree insertion
bplus_tree = BPlusTree(5)  # Initialize a B+ tree with minimum degree 5
start_time = time.perf_counter()  # Start timer for B+ tree insertion

# TODO: Insert each row into the B+ tree
for _, (k, v) in data.iterrows():
    bplus_tree.insert(k, v)
end_time = time.perf_counter()  # End timer for B+ tree insertion

# TODO: Calculate elapsed time for B+ tree
bplus_tree_time = end_time - start_time

# In[ ]:


# --- Print Results ---
# TODO: Print the B-tree and its insertion time
print(f'\nPrinting BTree...\n')
btree.print_tree()
print('btree_time:',btree_time, '\n')

# In[ ]:


# TODO: Print the B+ tree and its insertion time
print(f'\nPrinting BPlusTree...\n')
bplus_tree.print_tree()
print('bplus_tree_time:',bplus_tree_time)

# In[ ]:





# In[ ]:





# In[ ]:




