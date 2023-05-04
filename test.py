from Getty_Query_Class import Getty_TGN_Request
from Getty_Query_Class import Getty_TGN_Location
from pathlib import Path

from rdflib import Graph
from rdflib import URIRef


def main():
    # retrieved = Getty_TGN_Request('Tunganhsien', save_to_folder='dump2')
    # retrieved.print_findings()
    # retrieved.save_findings('dump')
    folder = Path('dump2')
    for file in folder.iterdir():
        if file.suffix == '.rdf':
            location = Getty_TGN_Location(folder, file.name)
            print(location.prettify(25))
                
    
    
    # file = Path('Tunganhsien-Baiyashi-inhabited place-8201269.rdf')
    # if (full_path:=folder/file).exists():
    #     location = Getty_TGN_Location(folder, file)
    #     print(location.latitude, location.longitude)
    
    # g = Graph()
        
    # subject = URIRef("http://vocab.getty.edu/tgn/8201269-geometry")
    # pred_lat =URIRef("http://vocab.getty.edu/resource?uri=http%3A%2F%2Fschema.org%2Flatitude")
    # uri_lat = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat")
    # uri_long = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long")
    
    # a = URIRef('http://schema.org/latitude')
        
    # g.parse('tgn_8201269(1).ttl', format='n3')
    # # g.print()
    # latitude_uri = URIRef('http://schema.org/latitude')
    # longitude_uri = URIRef('http://schema.org/longitude')
    # # latitude_literal = g.value(subject=URIRef('http://vocab.getty.edu/tgn/8201269-geometry'),
    # #                        predicate=latitude_uri)
    # # print(latitude_literal)
    
    # for s,p,o in g:
    #     if p == URIRef('http://schema.org/latitude'):
    #         print (o)
        


if __name__ == '__main__':
    main()


# a_string = "Zixishi (fourth level subdivision) [8687656], Hunan (province) [7002079], China (nation) [1000111], Asia (continent) [1000004], World (facet) [7029392]"

# data = _extract_data(a_string)
# print(data)