import sys, os
sys.path.append('../')

from getEUtilsInfo import citationCount,extractFromXML,getIndraQueryTermStmtCount

def test_citationCount():
    pmid = "32628996"
    assert citationCount(pmid)==0

def test_extractFromXML():
    os.environ["INDRA_DB_REST_URL"] = "https://db.indra.bio"
    pmid = "32628996"
    term = "DMRT1"
    extractFromXML(pmid, term)
    assert os.path.exists("eutils_output.tsv")

def test_getIndraQueryTermStmtCount():
    assert type(getIndraQueryTermStmtCount("DMRT1")) is int