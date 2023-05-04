from dataclasses import dataclass
import requests
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
from pathlib import Path
from rdflib import Graph
from rdflib import URIRef


@dataclass
class Getty_TGN_Block_Data:
    """This is the dataclass used to save all the data from the results of the query on the Getty TGN website"""

    name: str
    type: str
    id: int
    _max_length: int = 0

    def __post_init__(self):
        try:
            self.id = int(self.id)
        except ValueError:
            "Getty_TGN_Block_Data: The id value is not convertible to int"
        self._max_length = max(len(self.name), len(self.type), len(str(self.id)))

    def get_data_list(self) -> list:
        return [self.name, self.type, str(self.id)]

    def get_rdf_link(self) -> str:
        return f"http://vocab.getty.edu/tgn/{self.id}.rdf"


class Getty_TGN_Location:
    def __init__(self, folder: str | Path, rdf_file: str) -> None:
        """Class:
        This class manages the acquisition of the coordinates
        from the rdf file
        """
        if type(folder) == Path or issubclass(type(folder), Path):
            self._folder = folder
        elif type(folder) == str:
            self._folder = Path(folder)
        else:
            raise TypeError("{type(folder)} is not supported")
        self._filename = Path(rdf_file)
        self._data = self.get_data()
        if self._filename.suffix != ".rdf":
            raise ValueError(
                f"Getty_TGN_Location: {self._filename.name} is not an rdf file"
            )

        self.query_name = self._filename.name.split("-")[0]
        self.result_name = self._filename.name.split("-")[1]
        self.result_type = self._filename.name.split("-")[2]
        self.result_id = self._filename.name.split("-")[3].split(".")[0]
        self.latitude, self.longitude = self.get_coordinates()

    def get_data(self) -> str:
        """Get the data from the file as a string"""
        return Path(self._folder, self._filename).read_text(encoding="utf-8")

    def get_coordinates(self) -> tuple:
        """Gets the coordinates from the rdf file"""
        g = Graph()
        uri_lat = URIRef("http://schema.org/latitude")
        uri_long = URIRef("http://schema.org/longitude")
        latitude = None
        longitude = None
        g.parse(self._folder / self._filename)
        for _s, p, o in g:
            if p == uri_lat:
                latitude = float(o)
            if p == uri_long:
                longitude = float(o)
        return (latitude, longitude)

    def prettify(self, indent: int = 0) -> str:
        """Format the class attributes into a string with tabs separating the fields"""
        return (
            f"{self.query_name: <{indent}}\t"
            f"{self.result_name: <{indent}}\t"
            f"{self.result_type: <{indent}}\t"
            f"{self.result_id: <{indent}}\t"
            f"{self.latitude: <{indent}}\t"
            f"{self.longitude: <{indent}}"
        )


class Getty_TGN_Request:
    """Class to manage a request of a query to GETTY_TGN Online Database"""

    def __init__(
        self,
        query_name: str,
        query_placetypeid: str = "",
        query_nationid: str = "",
        save_to_folder: str = "",
    ) -> None:

        _mainlink = (
            "http://vocabsservices.getty.edu/TGNService.asmx/TGNGetTermMatch?name="
        )
        _placetype_attr = "misr&placetypeid="
        _nation_attr = "&nationid="

        self.queryname = query_name
        self.querytype = query_placetypeid
        self.querynation = query_nationid

        self._link = (
            f"{_mainlink}%22{query_name}%22"
            f"{_placetype_attr}%22{query_placetypeid}%22"
            f"{_nation_attr}%22{query_nationid}%22"
        )

        response = requests.get(self._link)
        self.findings = self._XML_find_subjects(
            BeautifulSoup(response.text, "html.parser").prettify()
        )

        if save_to_folder:
            self.save_findings(save_to_folder)
        # self._status = ""

    def _XML_find_subjects(self, xml) -> list:
        tree = ET.fromstring(xml)
        returnlist = []
        for element in tree.iter("preferred_parent"):
            returnlist.append(self._extract_data(element.text))
        return returnlist

    def _extract_data(self, data: str) -> dict:
        """take a string organized as:
        A (Atype) [Acode], B (Btype) [Bcode], ...
        and return a list of dicts with name:A, type:Atype, id:Acode..."""
        nodes = data.strip().rstrip("]").split("], ")
        all_nodes = []
        for node in nodes:
            node = node.replace(" (", "@").replace(") [", "@")
            blocks = node.split("@")
            datum = Getty_TGN_Block_Data(
                blocks[0].strip(), blocks[1].strip(), blocks[2].strip()
            )
            all_nodes.append(datum)
        return all_nodes

    def print_findings(self):
        """pretty print of self.findings"""
        max = 0
        for i, finding in enumerate(self.findings):
            print(f"Result {i}:")
            for block in finding:
                if block._max_length > max:
                    max = block._max_length + 3
            for block in finding:
                print(f"{block.name : <{max}}{block.type : <{max}}{block.id : <{max}}")
            print("-------")

    def save_findings(self, folder):
        for finding in self.findings:
            filename = Path(
                self.queryname
                + "-"
                + self.querynation
                + "-".join(finding[0].get_data_list())
                + ".rdf"
            )
            retrieved = requests.get(finding[0].get_rdf_link()).text
            Path(folder).mkdir(exist_ok=True)
            full_path = folder / filename
            with full_path.open(mode="w", encoding="utf-8") as file:
                file.write(retrieved)
