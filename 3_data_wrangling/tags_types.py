
# coding: utf-8

# # Audit Tags Keys

# Before start working on the OSM data, let's check the key values and see their pattern. This will be done through using 3 regular expressions then will count four tag categories in a dictionary:
# - "lower": for tags that contain only lowercase letters and are valid
# - "lower_colon": for otherwise valid tags with a colon in their names
# - "problemchars": for tags with problematic characters
# - "other": for other tags that do not fall into the other three categories

# In[1]:

import xml.etree.cElementTree as ET
import pprint
import re


# In[2]:

osm_file = open("san-jose_california.osm", "r") 


# In[3]:

# the regular expressions that will be used to audit the tags keys
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[4]:

def key_type(element, keys):
    '''find the type for a key'''
    if element.tag == "tag":
        k_value = element.attrib['k'] # targeted value
        if re.search(lower, k_value):
            keys['lower'] += 1
        elif re.search(lower_colon, k_value):
            keys['lower_colon'] += 1
        elif re.search(problemchars, k_value):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    
    return keys


# In[5]:

def process_map(filename):
    '''parse through the OSM and check the key_type for each key and count their numbers'''
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for event, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys


# In[6]:

# print the count results
pprint.pprint(process_map(osm_file))

