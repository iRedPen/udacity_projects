
# coding: utf-8

# # Audit of Street Names

# Here I'll extract the unexpected street types and change them to the appropriate ones in the expected list.

# In[1]:

# needed libraries
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[2]:

osm_file = "san-jose_california - Copy.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # Regular Exp to extract the type (last word in the street name)


# In[3]:

# expected street types
expected = ['Street', 'Road', 'Avenue', 'Boulevard', 'Circle', 'Court', 'Drive', 'Expressway', 'Highway', 'Lane', 
            'Parkway', 'Place', 'Square', 'Terrace', 'Way', ]


# In[4]:

def audit_street_type(street_types, street_name):
    '''extract street type using re'''
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# In[5]:

def is_street_name(elem):
    '''to check if the key is for street'''
    return (elem.attrib['k'] == "addr:street") 


# In[6]:

def audit_street_name(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set) #dictunary for unexpected street types with their street names
    for event, elem in ET.iterparse(osm_file, events=("start",)): 
        if elem.tag == "node" or elem.tag == "way": 
            for tag in elem.iter("tag"):
                if is_street_name(tag): 
                    audit_street_type(street_types, tag.attrib['v']) #check if audited street type is in expected list
    osm_file.close()
    return street_types


# In[7]:

pprint.pprint(dict(audit_street_name(osm_file)))


# In[8]:

# map corrections needed based on the above output
mapping = {
            'Ave':'Avenue',
            'Blvd':'Boulevard',
            'Blvd.':'Boulevard',
            'Boulvevard':'Boulevard',
            'Cir':'Circle',
            'Ct':'Court',
            'Dr':'Drive',
            'Hwy':'Highway',
            'Ln':'Lane',
            'Rd':'Road',
            'Sq':'Square',
            'St':'Street',
            'ave':'Avenue',
            'court':'Court',
            'street':'Street'
            }


# In[9]:

def update_name(name, mapping):
    '''update name if found in mapping'''
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = street_type_re.sub(mapping[street_type], name)
    return name


# In[13]:

# parse file to update names
street_types = audit_street_name(osm_file)
for street_type, ways in street_types.iteritems():
    for name in ways:
        if name != update_name(name, mapping): # if there is an update of the name
            better_name = update_name(name, mapping) # update name to
            print name, "=>", better_name


# In[ ]:



