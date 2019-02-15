
# coding: utf-8

# # SQL Queries

# Here we will use the DB API to do some queries on the OSM Database.

# In[1]:

import sqlite3
import pprint


# In[2]:

connection = sqlite3.connect("osm.db") #connecting with the database


# In[3]:

cursor = connection.cursor() # cursor used to run queries and fetch results


# In[4]:

# Count number of ways
cursor.execute("SELECT COUNT(*) FROM ways")
results = cursor.fetchall()
print results


# In[5]:

# Count number of nodes
cursor.execute("SELECT COUNT(*) FROM nodes")
results = cursor.fetchall()
print results


# In[6]:

# Count number of unique users
cursor.execute("SELECT COUNT(DISTINCT(user)) FROM (SELECT user FROM nodes UNION SELECT user FROM ways )")
results = cursor.fetchall()
print results


# In[7]:

# Top 10 contributing users
cursor.execute("SELECT user, count(*) as freq FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) GROUP BY user ORDER BY freq DESC LIMIT 10")
results = cursor.fetchall()
pprint.pprint(results)


# In[8]:

# Most frequant amenity types
cursor.execute("SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='amenity' GROUP BY value ORDER BY freq DESC LIMIT 10")
results = cursor.fetchall()
pprint.pprint(results)


# In[9]:

# Most popular cusion
cursor.execute("SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='cuisine' GROUP BY value ORDER BY freq DESC LIMIT 10")
results = cursor.fetchall()
pprint.pprint(results)


# In[10]:

# Top 10 types of shops
cursor.execute("SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='shop' GROUP BY value ORDER BY freq DESC LIMIT 10")
results = cursor.fetchall()
pprint.pprint(results)


# In[11]:

# Most popular shop chain stores
cursor.execute("SELECT nt1.value, COUNT(*) as freq FROM nodes_tags as nt1 , nodes_tags as nt2 WHERE nt1.id=nt2.id AND nt2.key='shop' AND nt1.key='name' GROUP BY nt1.value ORDER BY freq DESC LIMIT 10")
results = cursor.fetchall()
pprint.pprint(results)


# In[12]:

# Volume of contripution per year
# Here I'll use the strftime() to extract the year from the timestamp. Ref: https://sqlite.org/lang_datefunc.html
cursor.execute("SELECT strftime('%Y',timestamp) as month, count(*) as freq FROM ways GROUP BY month ORDER BY freq DESC")
results = cursor.fetchall()
pprint.pprint(results)

