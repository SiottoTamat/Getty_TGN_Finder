import requests
from bs4 import BeautifulSoup
import re
import xml.etree.cElementTree as ET


def download_from_id(id: str) -> str:
    """download the RTL file from Getty_TGN with the id provided
       returns a string"""
    link = f"http://vocab.getty.edu/tgn/{id}.rdf"
    request = requests.get(link)
    return request.text


def save_string(filename, astring):
    with open(filename,'w', encoding='utf8') as file:
        file.write(astring)


def replace_all(a_string, old: list, new: str) -> str:
    for char in old:
        a_string = a_string.replace(char, new)
    return a_string


def extract_data(data: str) -> dict:
    focus = replace_all(data.split(',')[0], ["(", ")", "[", "]"], "@").split('@')
    return {"name": focus[0].strip(),
            "type": focus[1].strip(),
            "id": focus[3].strip()
            }


def XML_find_subjects(xml) -> list:
    tree = ET.fromstring(xml)
    returnlist = []
    for element in tree.iter('preferred_parent'):
        returnlist.append(extract_data(element.text))
    return returnlist
        

def main():
    link_1 = "http://vocabsservices.getty.edu/TGNService.asmx/TGNGetTermMatch?name=%22Tunganhsien%22misr&placetypeid=&nationid=%22China%22"
    link = "https://www.getty.edu/vow/TGNServlet?find=Tunganhsien&place=&nation=China&prev_page=1&page=1&english=N"
    link_3 = "http://vocab.getty.edu/tgn/8201269.rdf"
    
    
    response = requests.get(link_1)
    print(response.content)
    page_text = response.text
    soup = BeautifulSoup(page_text, "html.parser")
    findings = XML_find_subjects(soup.prettify())
    
    for finding in findings:
        id = finding['id']
        save_string(f"{id}.rdf",download_from_id(id))
    #  print(findings)
    

if __name__ == '__main__':
    main()
