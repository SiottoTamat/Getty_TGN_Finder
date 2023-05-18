# Getty_TGN_Finder
This small library allows to query the Getty Thesaurus of Geographic Names (TGN). 
Getty TGN is a structured vocabulary of geographic names for indexing art and architecture
information in Getty repositories. It contains over 1.3 million names for places, regions,
and physical features around the world. The TGN is available online through the Getty's website
and can be accessed by anyone free of charge.

The TGN includes not only current geographic names, but also historical and vernacular names,
as well as variant spellings and names in multiple languages. It provides information about the
hierarchical relationships between places, and also includes information about the administrative
divisions, cultural and physical features, and geographic coordinates of each place.

The TGN is used by museums, libraries, and other cultural heritage institutions to provide
standardized access to geographic information for their collections. It can also be used by
researchers and individuals interested in studying the history and geography of a particular
region or place.

## Example Code
```python
from Getty_Query_Class import Getty_TGN_Request
from Getty_Query_Class import Getty_TGN_Location
from pathlib import Path

list_names = ["Fort Perovsky", "Peking", "Amsterdam Island", "NonePlace001"]

savefolder = "SaveFolder"
# find the results of each query and save them in the SaveFolder
# print all the results of each query
for name in list_names:
    print(f"{name}:\n")
    retrieved = Getty_TGN_Request(name, save_to_folder=savefolder)
    if retrieved.findings:
        retrieved.print_findings()
    else:
        print(f"{name} not found\n\n")
# for each json file downloaded, create a Getty_TGN_Location object.
# print the prettified version of the object.
folder = Path(savefolder)
for file in folder.iterdir():
    if file.suffix == ".jsonld":
        location = Getty_TGN_Location(folder, file.name)
        print(location.prettify(5))
```
**result:**
```python
Fort Perovsky:

Result 0:
Kyzylorda         inhabited place   7010344
Qyzylorda         province          1003384
Kazakhstan        nation            7014786
Asia              continent         1000004
World             facet             7029392
-------
Peking:

Result 0:
Bai He    stream    8213312
China     nation    1000111
Asia      continent 1000004
World     facet     7029392
-------
Result 1:
Beijing           inhabited place   7001758
Beijing Shi       municipality      1000956
China             nation            1000111
Asia              continent         1000004
World             facet             7029392
-------
Result 2:
Beijing Shi       municipality      1000956
China             nation            1000111
Asia              continent         1000004
World             facet             7029392
-------
Result 3:
Kosciusko                   inhabited place             2056763
Attala county               county                      2001089
Mississippi                 state                       7007522
United States               nation                      7012149
North and Central America   continent                   1000001
World                       facet                       7029392
-------
Result 4:
Peking                      inhabited place             7119857
Saxony-Anhalt               state                       7003687
Germany                     nation                      7000084
Europe                      continent                   1000003
World                       facet                       7029392
-------
Amsterdam Island:

Result 0:
Île Amsterdam                         island                                1006266
French Southern and Antarctic Lands   overseas territory                    1000163
France                                nation                                1000070
Europe                                continent                             1000003
World                                 facet                                 7029392
-------
NonePlace001:

NonePlace001 not found


Amsterdam Island        Île Amsterdam   island  1006266 77.5333 -37.8667
Fort Perovsky   Kyzylorda       inhabited place 7010344 65.4667 44.8667
Peking  Bai He  stream  8213312 116.836399      40.558191
Peking  Beijing Shi     municipality    1000956 116.416667      40.2
Peking  Beijing inhabited place 7001758 116.388869      39.928819
Peking  Kosciusko       inhabited place 2056763 -89.5833        33.05
Peking  Peking  inhabited place 7119857 11.116667       52.083333
```


## Getty_TGN_Request class 
Overall, the Getty_TGN_Request class provides a convenient way to query the Getty Thesaurus of Geographic Names online database and retrieve data for specific places.
The class is used to manage a request for a query to the Getty Thesaurus of Geographic Names (TGN) online database. 

To retrieve a query, you can simply create an instance of the class; if you desire to automatically save the jsonld files, you can specify the folder name with the optional argument 'save_to_folder' as in the example below:

`retrieved = Getty_TGN_Request('query', save_to_folder='query_folder')`



**This class has the following methods and attributes:**

### __init__ method
The constructor for this class takes the following parameters:

query_name: a string that represents the name of the place to search for.
query_placetypeid: a string that represents the ID of the place type to search for (optional).
query_nationid: a string that represents the ID of the nation to search for (optional).
save_to_folder: a string that represents the path of the folder to save the results in (optional).
Upon initialization, the _mainlink, _placetype_attr, and _nation_attr variables are used to construct a URL to query the TGN online database with the provided parameters. The query results are then parsed and stored in the findings attribute. If a save_to_folder is provided, the results are saved to files in the specified directory.

### _XML_find_subjects method
This method takes an XML string as an input and returns a list of dictionaries that contain information about the found places. It first parses the XML string with ElementTree and then iterates over the preferred_parent elements to extract the data for each place.

### _extract_data method
This method takes a string that is organized as "A (Atype) [Acode], B (Btype) [Bcode], ..." and returns a list of dictionaries with the name, type, and ID of each place. It first splits the input string into individual nodes and then extracts the data for each node by replacing characters and splitting the resulting strings.

### print_findings method
This method prints the findings attribute in a readable format to the console. It first determines the maximum length of each block of data for all the found places and then prints each block of data for each place with the maximum length determined earlier.

### save_findings method
This method saves the results of the query to files in the specified directory. It first constructs a filename based on the query parameters and the data extracted from the first place in the findings list. It then retrieves the jsonld data for the first place in the findings list and saves it to a file in the specified directory with the constructed filename.


## The Getty_TGN_Location class:
It manages the acquisition of the coordinates from the jsonld file. The class takes two arguments: **folder** and **jsonld_file**. The folder argument specifies the directory path where the jsonld file is located, and the jsonld_file argument specifies the jsonld file name. If the folder argument is a string, it will be converted to a Path object. 

### The **__init__** method 
Initializes several instance variables, such as _folder, _filename, _data, query_name, result_name, result_type, result_id, **latitude**, and **longitude**. 

### get_data method 
Returns the contents of the jsonld file as a string. 

### get_coordinates method 
Extracts the latitude and longitude coordinates from the jsonld file. 

### prettify method 
Formats the class attributes into a string with tabs separating the fields.
