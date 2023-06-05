from bs4 import BeautifulSoup
import urllib.request
import json
from pathlib import Path


def get_Getty_TGN_types() -> list | None:
    """gets the types of locations from the getty website and returns a list of them"""
    try:
        web_page = urllib.request.urlopen("https://www.getty.edu/vow/TGNPlacePopup")
        soup = BeautifulSoup(web_page.read(), "html.parser")
        locations = soup.find_all(name="input", attrs={"name": "place_type"})
        return [x["value"].strip() for x in locations]
    except Exception as e:
        print(f"failed to retrieve data:\n\t{e}")
        return None


def pickle_json(the_list: list, filename: Path | str = "Getty_Location_Types.json"):
    """Saves the content of the list as a json file"""
    if not isinstance(filename, Path) and type(filename) != str:
        raise ValueError(
            "pickle_json function error:\n\tFilename must be a string or pathlib.Path"
        )
    if type(filename) == str:
        try:
            filename = Path(filename)
        except Exception as e:
            print(f"Failed to create the file {filename}:\n\t{e}")

    if type(the_list) != list:
        raise ValueError("pickle_json function error:\n\talist must be of type list")

    if filename.suffix != ".json":
        filename = filename.with_suffix(".json")
    filename.write_text(json.dumps(the_list))


def unpickle_json(filename: str | Path) -> list:
    """Unpickles the json with all the location type definitions as a list"""
    if not isinstance(filename, Path) and type(filename) != str:
        raise ValueError(
            "pickle_json function error:\n\tFilename must be a string or pathlib.Path"
        )
    if type(filename) == str:
        try:
            filename = Path(filename)
        except Exception as e:
            print(f"Failed to create the file {filename}:\n\t{e}")
    with filename.open() as file:
        json_data = json.load(file)
    return json_data
