
# OSM Data Wrangling Project Report


## Introduction

[OpenStreetMap (OSM)](https://www.openstreetmap.org/)  is a collaborative project to create a free editable map of the world.
In this project, I'll extract a city's map data as an XML format. Then, I'll parse through it to identify some of the inconsistencies of the entered data and do programming corrections to it. After that, I'll transform the data to a tabular form (csv) so it can be imported to an SQL Database. Finally, I'll use a number of database queries to provide a an overview of some elements.

## Selected Map

### San Jose, California, USA 

![alt text](https://klokantech-0.tilehosting.com/styles/basic/static/auto/500x500@2x.png?key=PEzWaC5IFbhtXyxlyrI&path=-122.046%2C37.125%7C-122.046%2C37.469%7C-121.589%2C37.469%7C-121.589%2C37.125%7C-122.046%2C37.125&stroke=%235A8500 "San Jose OSM")


I chose San Jose because it's the city that tops my wish list for its status as [a knowledge capital and an innovation frontier](https://www.brookings.edu/wp-content/uploads/2016/09/metro_20160928_gcitypes.pdf).

**The XML Data was downloaded from [a preselected metro area from the OSM's Map Zen](https://mapzen.com/data/metro-extracts/metro/san-jose_california/). The size of the uncompressed OSM XML file is around 375MB.**

## Data Overview

Before starting to audit so of the data elements, I wanted to get a sense of the size of the data. So, using ***tag_count.py*** I checked what aare types of tags are in the data and how many of each. The result was:

```
{'bounds': 1,
 'member': 20036,
 'nd': 2058266,
 'node': 1764115,
 'osm': 1,
 'relation': 2089,
 'tag': 738863,
 'way': 236211}
```

After that, I checked the key tags for the element "tag", there was 939 different tags. Here is the list of the most occuring:

```
 ('building', 137946),
 ('highway', 90710),
 ('name', 49700),
 ('tiger:county', 31957),
 ('tiger:name_base', 28780),
 ('tiger:name_type', 27641),
 ('tiger:cfcc', 25800),
 ('addr:housenumber', 22443),
 ('addr:street', 22062),
 ('oneway', 16696),
 ('service', 16479),
 ('tiger:reviewed', 13918),
 ('addr:postcode', 13147),
 ('surface', 11541),
 ('height', 11078),
 ('source', 10971),
 ('lanes', 10246),
 ('amenity', 8200),
 ('maxspeed', 7866),
 ('cycleway', 6312),
 ('addr:city', 6070)
```

Now, using ***tags_count.py*** let's check these key tags and see what their pattern based on 3 regular expressions then will categorize them in four groups:
* "lower": for tags that contain only lowercase letters and are valid
* "lower_colon": for otherwise valid tags with a colon in their names
* "problemchars": for tags with problematic characters
* "other": for other tags that do not fall into the other three categories

The results was as follow:
```
{'lower': 484799, 'lower_colon': 231731, 'other': 22332, 'problemchars': 1}
```

The key tag with the problematic characters is: `service area`

## Data Audit

I selected three of the most commen `addr:` tags to audit.

### Audit of Street Names
In ***street_audit.py***, I used a regular expression to extract the last word of the `addr:street` values, which will be usually the street type. 

After that, I got all the unexpectedstreet types with their corresponding streets and found a lot of inconsistancies, which can be categorized as follow:

__* Abbreviation:__

``` 'Rd': set(['Berryessa Rd',
            'Homestead Rd',
            'Mt Hamilton Rd',
            'Mt. Hamilton Rd',
            'Quimby Rd',
            'San Antonio Valley Rd',
            'Saratoga Los Gatos Rd',
            'Silver Creek Valley Rd',
            'Wolfe Rd'])```
            
__* Wrong spelling: __

``` 'Boulvevard': set(['Los Gatos Boulvevard'])```

__* Lower case:__

```  'court': set(['Cortona court']), 'street': set(['N 1st street'])```

Then, I used this code to update the names:
``` Python
def update_name(name, mapping):
    '''update name if found in mapping'''
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = street_type_re.sub(mapping[street_type], name)
    return name
# parse file to update names
street_types = audit_street_name(osm_file)
for street_type, ways in street_types.iteritems():
    for name in ways:
        if name != update_name(name, mapping): # if there is an update of the name
            better_name = update_name(name, mapping) # update name to
            print name, "=>", better_name
```

Here is the output:
```
Gaundabert Ln => Gaundabert Lane
Barber Ln => Barber Lane
Branham Ln => Branham Lane
Wolfe Rd => Wolfe Road
Mt Hamilton Rd => Mt Hamilton Road
Berryessa Rd => Berryessa Road
Saratoga Los Gatos Rd => Saratoga Los Gatos Road
Quimby Rd => Quimby Road
San Antonio Valley Rd => San Antonio Valley Road
Homestead Rd => Homestead Road
Mt. Hamilton Rd => Mt. Hamilton Road
Silver Creek Valley Rd => Silver Creek Valley Road
wilcox ave => wilcox Avenue
Cortona court => Cortona Court
Monterey Hwy => Monterey Highway
Fountain Oaks Dr => Fountain Oaks Drive
Minto Dr => Minto Drive
1350 S Park Victoria Dr => 1350 S Park Victoria Drive
Linwood Dr => Linwood Drive
1490 S Park Victoria Dr => 1490 S Park Victoria Drive
Samaritan Dr => Samaritan Drive
Evergreen Village Sq => Evergreen Village Square
N 5th St => N 5th Street
Monroe St => Monroe Street
Casa Verde St => Casa Verde Street
Celadon Cir => Celadon Circle
Los Gatos Boulvevard => Los Gatos Boulevard
N 1st street => N 1st Street
Los Gatos Blvd => Los Gatos Boulevard
Mission College Blvd => Mission College Boulevard
Stevens Creek Blvd => Stevens Creek Boulevard
Santa Teresa Blvd => Santa Teresa Boulevard
Palm Valley Blvd => Palm Valley Boulevard
N McCarthy Blvd => N McCarthy Boulevard
McCarthy Blvd => McCarthy Boulevard
Cherry Ave => Cherry Avenue
Saratoga Ave => Saratoga Avenue
Greenbriar Ave => Greenbriar Avenue
Blake Ave => Blake Avenue
Foxworthy Ave => Foxworthy Avenue
Hillsdale Ave => Hillsdale Avenue
N Blaney Ave => N Blaney Avenue
Meridian Ave => Meridian Avenue
Westfield Ave => Westfield Avenue
The Alameda Ave => The Alameda Avenue
Seaboard Ave => Seaboard Avenue
Walsh Ave => Walsh Avenue
E Duane Ave => E Duane Avenue
W Washington Ave => W Washington Avenue
1425 E Dunne Ave => 1425 E Dunne Avenue
Cabrillo Ave => Cabrillo Avenue
Hollenbeck Ave => Hollenbeck Avenue
Los Gatos Blvd. => Los Gatos Boulevard
Perivale Ct => Perivale Court```

### Audit of Postcodes

In ***postcode_audit.py***, I parsed through the `addr:postcode` and found three different types of postcodes:
* Postcode with only zipcode (5 digits only): `'95148'`
* Postcode with additional 4 digits (added after the zipcode). Somecases have 3 digits: ` '95014-5263'`
* Postcode starting with two letters (state abbreviation): `'CA 94035'`

Then, to make the data consistent I used this code to update the postcodes to have only the 5 digits zipcode.
``` Python
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
```

And here is a sample of the output:
```
95014-2522 => 95014
CA 95110 => 95110
95014-2456 => 95014
95014-2456 => 95014
95014-2405 => 95014
95014-246 => 95014
95014-246 => 95014
95014-2105 => 95014
95014-2105 => 95014
95037-4128 => 95037
95037-4132 => 95037
95037-9241 => 95037
95014-1702 => 95014
```

### Audit of City Name 
In ***city_audit.py***, I audited the values for `addr:city` and counted them in a dictionary.
```
{'Alviso': 11,
 'Campbell': 75,
 'Campbelll': 3,
 'Coyote': 1,
 'Cupertino': 60,
 'Felton': 1,
 'Fremont': 1,
 'Los Gato': 1,
 'Los Gatos': 145,
 'Los Gatos, CA': 1,
 'Milpitas': 104,
 'Moffett Field': 1,
 'Morgan Hill': 388,
 'Mountain View': 7,
 'Mt Hamilton': 1,
 'Redwood Estates': 1,
 'SUnnyvale': 1,
 'San Jose': 1025,
 u'San Jos\xe9': 159,
 'San jose': 1,
 'Santa Clara': 323,
 'Santa clara': 1,
 'Saratoga': 230,
 'Sunnyvale': 3396,
 'Sunnyvale, CA': 1,
 'campbell': 1,
 'cupertino': 1,
 'los gatos': 1,
 'san Jose': 2,
 'san jose': 6,
 'santa Clara': 2,
 'santa clara': 1,
 'sunnyvale': 3}
```

San Jose itself was written in 5 different ways: 'San Jose', 'San José' *(with a diacritical mark on the e)*, 'San jose', 'san Jose' and 'san jose'.
Although 'San José' is the official name of the city, I decided to unify the name to 'San Jose' because it was more occurrent in the data.

Also, I found out that [since 1968, 'Alviso' is considered a neighborhood in San Jose not an independent city.](https://en.wikipedia.org/wiki/Alviso,_San_Jose,_California) So, I decided to change it also to 'San Jose'.

Here is the mapping that I used to update the names:
```
{
            'Alviso':'San Jose', 
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
```

## Data Exploration

After auditing the data, now it's time to explore it further. To do that, I transformed the data from a document format  to a tabular format, then write to 5 csv files, which are: "nodes.csv", "nodes_tags.csv", "ways.csv", "ways_nodes.csv" and "ways_tags.csv". The code used can be found in ***xml_to_csv.py***. 

Next, i imported in ***csv_to_sql.py*** these files to an SQL database "osm.db".

### File Sizes

File | Size 
:---: | :---: 
osm.db | 204 MB
nodes.csv | 145 MB
nodes_tags.csv | 3 MB
ways.csv | 13 MB
ways_nodes.csv | 49 MB
ways_tags.csv | 22 MB

### Queries
In ***queries.py***, I used some SQL queries to try to answer some questions from the data.

#### Number of Ways
SELECT COUNT(*) FROM ways
`236211`

#### Number of Nodes
SELECT COUNT(*) FROM nodes
`1764115`

#### Number of Unique Users
SELECT COUNT(DISTINCT(user)) FROM (SELECT user FROM nodes UNION SELECT user FROM ways
`1404`

#### Top Contributing Users
SELECT user, count(*) as freq FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways)
```[(u'andygol', 295528),
 (u'nmixter', 283796),
 (u'mk408', 142197),
 (u'Bike Mapper', 90929),
 (u'samely', 81019),
 (u'RichRico', 75936),
 (u'dannykath', 74146),
 (u'MustangBuyer', 64949),
 (u'karitotp', 62692),
 (u'Minh Nguyen', 51917)]```

This shows that the top two users contributed 29% of the data and the top 10 users contributed 61%.

#### Most Occurring Amenity Types
"SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='amenity' GROUP BY value ORDER BY freq DESC LIMIT 10"
```
[(u'restaurant', 885),
 (u'fast_food', 424),
 (u'bench', 313),
 (u'cafe', 258),
 (u'bicycle_parking', 206),
 (u'place_of_worship', 171),
 (u'toilets', 160),
 (u'school', 143),
 (u'bank', 130),
 (u'parking_space', 128)]
```

#### Most Popular Cuisines
"SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='cuisine' GROUP BY value ORDER BY freq DESC LIMIT 10"
```
[(u'vietnamese', 118),
 (u'mexican', 115),
 (u'sandwich', 96),
 (u'pizza', 91),
 (u'chinese', 88),
 (u'coffee_shop', 76),
 (u'japanese', 47),
 (u'indian', 46),
 (u'burger', 42),
 (u'american', 39)]
```

#### Most Occuring Shop Types
"SELECT value, COUNT(*) as freq FROM nodes_tags WHERE key='shop' GROUP BY value ORDER BY freq DESC LIMIT 10"
```
[(u'beauty', 128),
 (u'hairdresser', 125),
 (u'clothes', 115),
 (u'supermarket', 113),
 (u'car_repair', 92),
 (u'convenience', 91),
 (u'bakery', 53),
 (u'alcohol', 44),
 (u'mobile_phone', 42),
 (u'jewelry', 39)]
```

#### Most Occuring Shop Chain Stores
"SELECT nt1.value, COUNT(*) as freq FROM nodes_tags as nt1 , nodes_tags as nt2 WHERE nt1.id=nt2.id AND nt2.key='shop' AND nt1.key='name' GROUP BY nt1.value ORDER BY freq DESC LIMIT 10"
```
[(u'7-Eleven', 21),
 (u'Lucky', 11),
 (u'T-Mobile', 9),
 (u'AT&T', 7),
 (u'Target', 7),
 (u'Dollar Tree', 6),
 (u'FedEx Office Print and Ship Center', 6),
 (u'Verizon Wireless', 6),
 (u'BevMo', 5),
 (u'Great Clips', 5)]
```

#### Volume of Ways Contripution per Year
"SELECT strftime('%Y',timestamp) as month, count(*) as freq FROM ways GROUP BY month ORDER BY freq DESC"
```
[(u'2017', 98556),
 (u'2015', 52853),
 (u'2016', 37751),
 (u'2014', 15033),
 (u'2013', 10578),
 (u'2011', 7697),
 (u'2012', 5906),
 (u'2010', 4381),
 (u'2009', 2690),
 (u'2008', 673),
 (u'2007', 93)]
 ```
Althouth the contripution to San Jose's OSM started in 2007, this shows that 42% of the data was entered during this year and 80% of it since 2015.

## Ideas for Improvement

In this project, I worked on modifing three elements of the data, but still there is much more to do in them (e.g. correcting non-last words in street names) or other elements.
Still, I was really impressed with the open-source contribution that is visable in the OpenStreetMap and with the exponential growth of its size. However, it will be still a voluntry human efforts that are prone to contain errors but will be appriciated more if the data is more consistant and valid. 

One approch I suggest to limit the entry errors (e.g. abbreviation and misspelling) is to set clear, and maybe autometed, validation roles that will limit the variation. But this maybe will be difficult to achive accross countries and languages.
Another suggestion to validate the data is to allocate the best local experts (users with the highest contribution) to focus on validation. Also, they can be utilized to review mainly first-time users and communicate with them their observations and recommendations on their input. However, as shown in one of the queries above, there are vital few contributors who add the majority of the data, so maybe taking some of them to be only reviewers will affect the addition rate. So, there should be a way first to encourage more users to be activly part of this community.
