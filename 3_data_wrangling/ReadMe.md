OpenStreetMap (OSM) is a collaborative project to create a free editable map of the world. In this project, I'll extract a city's map data as an XML format. Then, I'll parse through it to identify some of the inconsistencies of the entered data and do programming corrections to it. After that, I'll transform the data to a tabular form (csv) so it can be imported to an SQL Database. Finally, I'll use a number of database queries to provide a an overview of some elements.

The files included are:
- selected_map.txt: link and description.
- tags_count.py:  to find what are the tags in the OSM data and how many for each.
- tags_types.py: audit key tags and see their pattern, compared to specified Regular Expressions.
- street_audit.py: audit street types.
- postcode_audit.py: audit postcodes.
- city_audit.py: audit city names.
- xml_to_csv.py: transform OSM data to csv.
- csv_to_sql.py: import csv files to SQL database.
- queries.py: queries to analyze the data.
- sample_extract.py: code to extract a sample from the original OSM xml.
- sample.osm: a sample OSM data.
- references.txt: web pages that were refered to throughout the project.
- report.md: document the data wrangling process and answer the rubric questions.
