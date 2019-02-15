
# coding: utf-8

# # OSM Sample Extract

# This code takes a systematic sample of elements from the original OSM file.
# 
# I selected a k value equal to 10 so the sample file size will be between 1-10 MB, as required in the project.
# 
# The code is taken from the the Project Details Page.

# In[3]:

#!/usr/bin/env python


import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "san-jose_california.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 40 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# In[ ]:



