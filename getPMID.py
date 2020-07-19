import requests
import time
import json
import xml.etree.ElementTree as ET

def _extractListID(filecontent, term):
    tree = ET.fromstring(filecontent, ET.XMLParser(encoding='utf-8'))
    ID = tree.findall('./IdList/Id')

    with open("pmid_list.txt", "a") as op_file:
        for i in ID:
            print(i.text + "~" + term, file=op_file)

"""
Get PMID for the Query terms
"""
def getPMID(terms):
    for term in terms:
        term = term.strip().rpartition(",")[0]
        flag = True
        while flag:
            try:
                xml_content = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=hasabstract%20AND%20"+term)
                _extractListID(xml_content.text, term)
                flag = False
            except:
                time.sleep(.5)

