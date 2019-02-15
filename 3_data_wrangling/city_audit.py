
# coding: utf-8

# # Audit for City Name

# Here I'll audit the tagged city names to insure they are consistent. 

# In[1]:

# Importing the needed libraries
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[2]:

osm_file = "san-jose_california.osm"


# In[3]:

def audit(osmfile):
    city_list = {} #dictunary to count the different city names
    for event, elem in ET.iterparse(osm_file, events=("start",)): #parsing the OSM file
        if elem.tag == "node" or elem.tag == "way": 
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:city": #required key
                    city_name = tag.attrib['v'] #value for the key (name of the city)
                    if city_name in city_list: # condition to check if was already found in the for loop or new
                        city_list[city_name] += 1 # add 1 if avilable 
                    else:
                        city_list[city_name] = 1 # assign 1 if new
    return city_list # updated list


# In[4]:

# printing the city audit results
pprint.pprint(audit(osm_file))


# In[8]:

# map the cities that need to be updated
mapping = {
            'Alviso':'San Jose', # a neighborhood in San Jose, not a city: 
            'Campbelll':'Campbell',
            'campbell':'Campbell',
            'cupertino':'Cupertino',
            'Los Gato':'Los Gatos',
            'Los Gatos, CA':'Los Gatos',
            'los gatos':'Los Gatos',
            'SUnnyvale':'Sunnyvale',
            'Sunnyvale, CA':'Sunnyvale',
            'sunnyvale':'Sunnyvale',
            u'San Jos\xe9':'San Jose',
            'San jose':'San Jose',
            'san Jose':'San Jose',
            'san jose':'San Jose',
            'santa Clara':'Santa Clara',
            'santa clara':'Santa Clara',
            'Santa clara':'Santa Clara',
            }


# In[9]:

# parse again to modify the city names, if needed
for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:city":
                    city_name = tag.attrib['v']
                    if city_name in mapping: #use mapping to update
                        better_name = city_name.replace(city_name,mapping[city_name])
                        print city_name, "=>", better_name # old and new names

