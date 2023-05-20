from dataclasses import dataclass
import xml.etree.cElementTree as ET
from pathlib import Path
import urllib.request
import json

__author__ = "Andrea Siotto"
__copyright__ = "MIT License"
__credits__ = ["Andrea Siotto"]
__license__ = "Undecided"
__version__ = "1.0"
__maintainer__ = "Andrea Siotto"
__email__ = "siotto.andrea@gmail.com"
__status__ = "Development"


@dataclass
class Getty_TGN_Element:
    """This is the dataclass used to save all the data from the
    results of the query on the Getty TGN website.
    """

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

    @property
    def link(self) -> str:
        return f"https://vocab.getty.edu/tgn/{self.id}"


class Getty_TGN_Location:
    def __init__(self, folder: str | Path, json_file: str) -> None:
        """Class:
        This class manages the acquisition of the coordinates
        from the json/jsonld file
        """
        if type(folder) == Path or issubclass(type(folder), Path):
            self._folder = folder
        elif type(folder) == str:
            self._folder = Path(folder)
        else:
            raise TypeError("{type(folder)} is not supported")
        self._filename = Path(json_file)
        self._data = self.get_data()
        if self._filename.suffix not in [".json", ".jsonld"]:
            raise ValueError(
                f"Getty_TGN_Location: {self._filename.name} is not an json or jsonld file"
            )

        self.query_name = self._filename.name.split("-")[0]
        self.result_name = self._filename.name.split("-")[1]
        self.result_type = self._filename.name.split("-")[2]
        self.result_id = self._filename.name.split("-")[3].split(".")[0]
        self.latitude, self.longitude = self.coordinates

    def get_data(self) -> str:
        """Get the data from the file as a string"""
        return Path(self._folder, self._filename).read_text(encoding="utf-8")

    @property
    def coordinates(self) -> tuple:
        file = self._folder / self._filename
        with open(file, "r") as f:
            data = json.load(f)
        for obj in data["identified_by"]:
            if obj.get("type") == "crm:E47_Spatial_Coordinates":
                aslist = json.loads(obj.get("value"))
                return tuple(aslist)
        return (None, None)

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


class Getty_TGN_Request_Json:
    """Class to manage a request of a query to GETTY_TGN Online Database.
    If you know the place type and/or the nation, it is strongly recommended
    to add them as parameters.
    If the parameter save_to_folder is set to a folder, then it automatically
    attempts to retrieve and save the json files of the results in the given folder.
    the important attribute is self.findings, which is a list of Getty_TGN_Element
    objects representing the results returned from the query. Each Gerry_TGN_Element
    records
    If there are no results for the query, self.findings is an empty list.

    """

    def __init__(
        self,
        query_name: str,
        query_placetypeid: str = "",
        query_nationid: str = "",
        save_to_folder: str = "",
    ) -> None:
        self.queryname = str(query_name)
        self.querytype = str(query_placetypeid)
        self.querynation = str(query_nationid)
        self.results: list(Getty_TGN_Element) = SOAP_Request(
            self.queryname, self.querytype, self.querynation
        )

        if save_to_folder:
            self.save_jsons(save_to_folder)

    def __str__(self):
        returned = f"Query: {self.queryname}\nType: {self.querytype}\nNation: {self.querynation}\nResults:\n"
        returned += self.pretty_results + "\n\n"
        return returned

    @property
    def pretty_results(self):
        """pretty print of self.results"""
        max = 0
        if not self.results:
            return "No results."
        returned = ""
        for i, finding in enumerate(self.results):
            returned += f"Result {i}:\n"
            for block in finding:
                if block._max_length > max:
                    max = block._max_length + 3
            for block in finding:
                returned += f"{block.name : <{max}}{block.type : <{max}}{block.id : <{max}}\n-------\n"
        return returned

    def save_jsons(self, folder):
        for finding in self.results:
            filename = Path(
                self.queryname
                + "-"
                + self.querynation
                + "-".join(finding[0].get_data_list())
                + ".jsonld"
            )
            try:
                #  the request has to have these specific headers
                baseurl = finding[0].link
                headers = {"Accept": "application/ld+json; charset=utf-8"}
                req = urllib.request.Request(baseurl, headers=headers)
                data = urllib.request.urlopen(req).read().decode("utf-8")

            except Exception as e:
                print(f"Error in retrieving the json file:\n\t{baseurl}\n\t{e}")
            #  create a json file in the folder given, load the json and save the prettified version json.dumps()
            Path(folder).mkdir(exist_ok=True)
            json_data = json.loads(data)
            full_path = folder / filename
            with full_path.open(mode="w", encoding="utf-8") as file:
                file.write(json.dumps(json_data, indent=4))


def SOAP_Request(
    query: str, query_type: str = "", query_nation: str = ""
) -> list(Getty_TGN_Element):
    """This class deals with the SOAP request to the server"""

    def _SOAP_find_results(xml_string: str) -> list:
        """This inner function get the string obtained by the request and return a list of all the results"""
        namespaces = {
            "soap": "http://www.w3.org/2003/05/soap-envelope",
            "tgn": "http://vocabsservices.getty.edu/",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        root = ET.fromstring(xml_string)
        nodes = root.findall(".//*Subject", namespaces)  # find all results of the query
        lines = []
        for node in nodes:
            dataline = node.iter(
                "Preferred_Parent"
            )  # extract the line with the results
            for data in dataline:
                lines.append(data.text)
        return lines

    def _extract_data(data: str) -> dict:
        """take a string organized as:
        A (Atype) [Acode], B (Btype) [Bcode], ...
        and return a list of dicts with name:A, type:Atype, id:Acode..."""
        nodes = data.strip().rstrip("]").split("], ")
        all_nodes = []
        for node in nodes:
            node = node.replace(" (", "@").replace(") [", "@")
            blocks = node.split("@")
            datum = Getty_TGN_Element(
                blocks[0].strip(), blocks[1].strip(), blocks[2].strip()
            )
            all_nodes.append(datum)
        return all_nodes

    # the strings for the SOAP request
    raw_request = (
        rf'<?xml version="1.0" encoding="utf-8"?>'
        rf"<soap12:Envelope "
        rf'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        rf'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        rf'xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">'
        rf"<soap12:Body>"
        rf'<TGNGetTermMatch xmlns="http://vocabsservices.getty.edu/">'
        rf"<name>{query}</name>"
        rf"<placetypeid>{query_type}</placetypeid>"
        rf"<nationid>{query_nation}</nationid>"
        rf"</TGNGetTermMatch>"
        rf"</soap12:Body>"
        rf"</soap12:Envelope>"
    )
    url = "http://vocabsservices.getty.edu/TGNService.asmx"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Content-Length": str(len(raw_request)),
    }

    try:
        # Create a POST request with the SOAP payload and headers
        req = urllib.request.Request(
            url, data=raw_request.encode("utf-8"), headers=headers
        )
        # Send the POST request and get the response
        response = urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error in connecting to SOAP server:\n\t{e}")
        return []
    return [
        _extract_data(x) for x in (_SOAP_find_results(response.read().decode("utf-8")))
    ]
