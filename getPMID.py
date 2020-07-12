import requests
import json
import xml.etree.ElementTree as ET

term_limit = 30
pmid_per_term_limit = 10


def extractListID(filecontent, term):
    tree = ET.fromstring(filecontent, ET.XMLParser(encoding='utf-8'))
    ID = tree.findall('./IdList/Id')

    with open("pmid_list.txt", "a") as op_file:
        for i in ID[0:pmid_per_term_limit]:
            print(i.text + "~" + term, file=op_file)


terms_request = requests.get(
    "https://raw.githubusercontent.com/cannin/reach-query/master/queries.csv")
terms = terms_request.text


for term in terms.splitlines()[1:(term_limit+1)]:
    term = term.strip().rpartition(",")[0]
    xml_content = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=hasabstract%20AND%20"+term)
    print("Term " + term)
    extractListID(xml_content.text, term)
