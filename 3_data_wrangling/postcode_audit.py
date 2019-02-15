
# coding: utf-8

# # Audit for Postcodes

# Here I'll audit the tagged postcodes to insure they are consistent. 

# In[1]:

# Importing the needed libraries
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[2]:

osm_file = "san-jose_california.osm"


# I want to see if there are any inconsistencies in the postcodes 

# In[3]:

def audit_postcodes(osmfile):
    '''check all the different postcodes in the OSM data'''
    postcodes = {} #dictunary to count the different postcode
    for event, elem in ET.iterparse(osm_file, events=("start",)): #parsing the OSM file
        if elem.tag == "node" or elem.tag == "way": 
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode": #required key
                    pc = tag.attrib['v'] #value for the key (postcode)
                    if pc in postcodes: # condition to check if was already found in the for loop or new
                        postcodes[pc] += 1 # add 1 if avilable 
                    else:
                        postcodes[pc] = 1 # assign 1 if new
    return postcodes # updated list


# In[4]:

# printing the postcodes audit results
pprint.pprint(audit_postcodes(osm_file))


# I can see that there are 3 main types of postcodes:
# * Postcode with only zipcode (5 digits only)
# * Postcode with additional 4 digits (added after the zipcode). Somecases have 3 digits (entry error).
# * Postcode starting with two letters (state abbreviation)
# 
# I'll update the second and third types to have only the zipcode

# In[5]:

def update(osmfile):
    '''correct the postcodes to make them consistant'''
    correct_postcode=re.compile(r'^\d{5}$') #only zipcode
    with_four_digits=re.compile(r'\d{5}-\d{3,4}$') # with additional 4 digits
    with_two_letters=re.compile(r'\w{2}\s\d{5}$') # with the state abbreviation
    for event, elem in ET.iterparse(osm_file, events=("start",)): #parsing the OSM file
        if elem.tag == "node" or elem.tag == "way": 
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode": #required key
                    postcode = tag.attrib['v'] #value for the key (postcode)
                    if correct_postcode.match(postcode): # check if there is no need to change
                        continue # no required changes
                    elif with_four_digits.match(postcode): #match the second type
                        updated_postcode = re.sub ('(\d{5})-\d{3,4}$', r'\1',postcode) # keep the zipcode only
                    elif with_two_letters.match(postcode): #match the third type
                        updated_postcode = re.sub ('\w{2}\s(\d{5})$', r'\1',postcode) # keep the zipcode only
                    print postcode , "=>", updated_postcode # print the updated postcodes
    return postcode

update(osm_file)

