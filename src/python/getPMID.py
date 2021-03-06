# getPMID.py

import requests
import time
import json
import xml.etree.ElementTree as ET


def _extractListID(filecontent, term):
    tree = ET.fromstring(filecontent, ET.XMLParser(encoding='utf-8'))
    ID = tree.findall('./IdList/Id')
    count = tree.find('./Count').text

    with open("pmid_list.txt", "a") as op_file:
        for i in ID:
            print(i.text + "~" + term + "~" + count, file=op_file)


def getPMID(terms, pmid_threshold=20):
    """
    Get PMID for the Query terms
    Parameters:
    terms: List of failed query terms
    pmid_threshold: Limit of Pubmed articles to process, default is 20
    """
    if pmid_threshold < 1:
        pmid_threshold = 20
    for term in terms:
        term = term.strip().rpartition(",")[0]
        flag = True
        while flag:
            try:
                xml_content = requests.get(
                    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax="+pmid_threshold+"&term=hasabstract%20AND%20"+term)
                _extractListID(xml_content.text, term)
                flag = False
            except:
                time.sleep(.5)
