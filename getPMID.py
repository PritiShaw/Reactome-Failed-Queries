import requests
import json
import xml.etree.ElementTree as ET

def _extractListID(filecontent, term):
    tree = ET.fromstring(filecontent, ET.XMLParser(encoding='utf-8'))
    ID = tree.findall('./IdList/Id')

    with open("pmid_list.txt", "w") as op_file:
        for i in ID:
            print(i.text + "~" + term, file=op_file)


terms_request = requests.get(
    "https://raw.githubusercontent.com/cannin/reach-query/master/queries.csv")
terms = terms_request.text

def getTerms(term_start, term_end):
    for term in terms.splitlines()[term_start:(term_end+1)]:
        term = term.strip().rpartition(",")[0]
        xml_content = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=hasabstract%20AND%20"+term)
        print("Term " + term)
        _extractListID(xml_content.text, term)
