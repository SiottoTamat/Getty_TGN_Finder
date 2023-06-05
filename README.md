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

The list of types of location is in the **location_types_pickled.json** file. If needed, you can
update the data using the function in the Getty_Location_Types module.

## Example Code
```python
from Getty_Query_Class import Getty_TGN_Request_Json
from Getty_Query_Class import Getty_TGN_Location
from pathlib import Path


def main():
    list_names = ["Fort Perovsky", "Peking", "Amsterdam Island", "NonePlace001"]

    savefolder = "Save_to"
    for name in list_names:
        retrieved = Getty_TGN_Request_Json(name, save_to_folder=savefolder)
        print(retrieved)

    folder = Path(savefolder)
    for file in folder.iterdir():
        if file.suffix == ".jsonld":
            location = Getty_TGN_Location(folder, file.name)
            print(location.prettify(5))


if __name__ == "__main__":
    main()
```
**result:**
```python
Query: Fort Perovsky
Type:
Nation:
Results:
Result 0:
Kyzylorda         inhabited place   7010344
-------
Qyzylorda         province          1003384
-------
Kazakhstan        nation            7014786
-------
Asia              continent         1000004
-------
World             facet             7029392
-------



Query: Peking
Type:        
Nation:
Results:
Result 0:
Bai He    stream    8213312
-------
China     nation    1000111
-------
Asia      continent 1000004
-------
World     facet     7029392
-------
Result 1:
Beijing           inhabited place   7001758
-------
Beijing Shi       municipality      1000956
-------
China             nation            1000111
-------
Asia              continent         1000004
-------
World             facet             7029392
-------
Result 2:
Beijing Shi       municipality      1000956
-------
China             nation            1000111
-------
Asia              continent         1000004
-------
World             facet             7029392
-------
Result 3:
Kosciusko                   inhabited place             2056763
-------
Attala county               county                      2001089
-------
Mississippi                 state                       7007522
-------
United States               nation                      7012149
-------
North and Central America   continent                   1000001
-------
World                       facet                       7029392
-------
Result 4:
Peking                      inhabited place             7119857
-------
Saxony-Anhalt               state                       7003687
-------
Germany                     nation                      7000084
-------
Europe                      continent                   1000003
-------
World                       facet                       7029392
-------



Query: Amsterdam Island
Type:
Nation:
Results:
Result 0:
Île Amsterdam                         island                                1006266
-------
French Southern and Antarctic Lands   overseas territory                    1000163
-------
France                                nation                                1000070
-------
Europe                                continent                             1000003
-------
World                                 facet                                 7029392
-------



Query: NonePlace001
Type:
Nation:
Results:
No results.


Amsterdam Island        Île Amsterdam   island  1006266 77.5333 -37.8667
Fort Perovsky   Kyzylorda       inhabited place 7010344 65.4667 44.8667
Peking  Bai He  stream  8213312 116.836399      40.558191
Peking  Beijing Shi     municipality    1000956 116.416667      40.2
Peking  Beijing inhabited place 7001758 116.388869      39.928819
Peking  Kosciusko       inhabited place 2056763 -89.5833        33.05
Peking  Peking  inhabited place 7119857 11.116667       52.083333
```


# Getty_TGN_Request_Json
Manages a request to the GETTY_TGN Online Database. It allows querying the database with optional parameters such as query name, place type ID, and nation ID. The class retrieves and stores the JSON results of the query. It uses the **SOAP_Request()** function to retrieve the results from the GETTY_TGN Online Database. It also utilizes the urllib.request module and the json module for retrieving and saving the JSON files.

The class has the following attributes and methods:

## Attributes:

queryname: A string representing the query name.
querytype: A string representing the place type ID.
querynation: A string representing the nation ID.
results: A list of Getty_TGN_Element objects that store the results of the query.

## Methods:

### __init__(): 
The class constructor that initializes the instance variables and performs the query. It takes parameters for the query name, place type ID, nation ID, and an optional parameter to specify a folder to save the JSON files of the results.
### __str__(): 
Returns a string representation of the object, including the query details and the pretty-printed results.
pretty_results: A property that returns a pretty-printed string representation of the query results.
### save_jsons(): 
Saves the JSON files of the query results to the specified folder.


# Getty_TGN_Location
Manages the acquisition of coordinates from a JSON or JSONLD file. 
The class checks the type of the folder parameter and converts it to a Path object if it is a string. It reads the JSON file, extracts the necessary information from the filename, and retrieves the latitude and longitude coordinates from the JSON data.
It has the following attributes and methods:

## Attributes:

_folder: A Path object representing the folder path where the JSON file is located.
_filename: A Path object representing the name of the JSON file.
_data: A string containing the data from the file.
query_name: A string representing the query name extracted from the filename.
result_name: A string representing the result name extracted from the filename.
result_type: A string representing the result type extracted from the filename.
result_id: A string representing the result ID extracted from the filename.
latitude: A float representing the latitude coordinate.
longitude: A float representing the longitude coordinate.

## Methods:

### __init__():
The class constructor that initializes the instance variables. It takes parameters for the folder path and the name of the JSON file.
### get_data():
Reads the data from the JSON file and returns it as a string.
### coordinates:
A property that retrieves the coordinates from the JSON data and returns them as a tuple of floats.
### prettify():
Formats the class attributes into a string with tabs separating the fields.


