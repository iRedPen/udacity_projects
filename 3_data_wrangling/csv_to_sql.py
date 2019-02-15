
# coding: utf-8

# #  Importing .csv Files Into a SQL Database

# Here, I'll import the 5 csv files into a SQL DB using the Schema provided in the project and using the code in this referance: 
# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python/30734789#

# In[1]:

# importing the needed libraries
import csv, sqlite3


# In[2]:

# initating and connecting the database
connection = sqlite3.connect("osm.db")
cur = connection.cursor()
connection.text_factory = str

# creating the nodes table
cur.execute("CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT);")

with open('nodes.csv','rb') as fin: 
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['lat'],i['lon'], i['user'],i['uid'], i['version'],i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes (id, lat,lon,user,uid,version,changeset,timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)
connection.commit()


# In[3]:

# creating the nodes_tags table

cur.execute("CREATE TABLE nodes_tags (id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes(id));") # use your column names here

with open('nodes_tags.csv','rb') as fin: 
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
connection.commit()


# In[4]:

# creating the ways table
cur.execute("CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT);") # use your column names here

with open('ways.csv','rb') as fin: 
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'],i['uid'], i['version'],i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id,user,uid,version,changeset,timestamp) VALUES (?,?,?,?,?,?);", to_db)
connection.commit()


# In[5]:

# creating the ways_tags table
cur.execute("CREATE TABLE ways_tags (id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, type TEXT, FOREIGN KEY (id) REFERENCES ways(id));") # use your column names here

with open('ways_tags.csv','rb') as fin: 
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
connection.commit()


# In[6]:

# creating the ways_nodes table
cur.execute("CREATE TABLE ways_nodes (id INTEGER NOT NULL, node_id INTEGER NOT NULL, position INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES ways(id), FOREIGN KEY (node_id) REFERENCES nodes(id));") # use your column names here

with open('ways_nodes.csv','rb') as fin: 
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'],i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?,?,?);", to_db)
connection.commit()


# In[7]:

# closing the connection
connection.close()

