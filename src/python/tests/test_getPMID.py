import sys, os, requests
sys.path.append('../')

from getPMID import _extractListID


def test_extractListID():
    term = "DMRT1"
    xml_content = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=hasabstract%20AND%20"+term)
    _extractListID(xml_content.text ,term)
    assert os.path.exists("pmid_list.txt")
