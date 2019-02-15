
# coding: utf-8

# # Count Tags

# Using iterative parsing, I want to what are the tags in the OSM data and how many for each.

# In[1]:

import xml.etree.cElementTree as ET
import pprint


# In[2]:

osm_file = open("san-jose_california.osm", "r") 


# In[3]:

def count_tags(filename):
    """find out what tags are in the OSM and how many for each"""
    tags = {}
    for event, element in ET.iterparse(filename):
        if element.tag in tags: # if in dict, add one to the count
            tags[element.tag] += 1
        else: # if not in dict, assign one to count
            tags[element.tag] = 1
    return tags


# In[4]:

pprint.pprint(count_tags(osm_file))


# In[5]:

osm_file.seek(0) # to return to the start of the OSM file
def count_keys(filename):
    """find out what are the key values of the tag "tag" in the OSM and how many for each"""
    keys = {}
    for event, element in ET.iterparse(filename):
        if element.tag == 'tag':
            if  element.attrib['k']:
                k_value = element.get('k')
                if k_value in keys:
                    keys[k_value] += 1
                else:
                    keys[k_value] = 1
    return keys


# In[6]:

# Before printing the keys, let's sort them based on the value in descending order
# Referance: https://stackoverflow.com/questions/35624064/sorting-dictionary-descending-in-python

keys_result = sorted(count_keys(osm_file).items() , key=lambda t : t[1] , reverse=True)
pprint.pprint(keys_result)


# In[7]:

len(keys_result) # number of different types of the k values for the tag "tag"

