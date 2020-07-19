import os
import gzip
import time
import sys
import csv
import requests
import json
import indra.literature.pubmed_client as parser
import xml.etree.ElementTree as ET
from indra.sources import indra_db_rest
from indra.assemblers.html.assembler import HtmlAssembler
from urllib.parse import urljoin
from indra.statements.statements import stmts_to_json


"""
Gets Citation count for PMID

Parameters
----------
pmid : string
    PMID of the medical paper

Returns
-------
string
    Citation Count
"""
def citationCount(pmid):
    flag = True
    while flag:
        try:
            citationCount_url = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&id="+pmid)
            flag = False
        except Exception as e:
            time.sleep(.5)
    try:
        fileContent = citationCount_url.text
        tree = ET.fromstring(fileContent, ET.XMLParser(encoding='utf-8'))
        ID = tree.findall('./LinkSet/LinkSetDb/Link')
        return len(ID)
    except:
        return 0


"""
Get number of statments generated by INDRA from the query term

Parameters
----------
    txt : string
        Query term to be processed
    source_apis : [], optional
        APIs to be searched from, default is all

Returns
------
    integer
        Number of Indra Statements
"""
def getIndraQueryTermStmtCount(txt, source_apis=None):
    grounding_service_url = 'http://grounding.indra.bio/'
    resp = requests.post(urljoin(grounding_service_url,
                                 'ground'), json={'text': txt})
    grounding_results = resp.json()
    if len(grounding_results) > 0:
        term_id = grounding_results[0]['term']['id']
        term_db = grounding_results[0]['term']['db']
        term = term_id + '@' + term_db
    else:
        return 0
    stmts = indra_db_rest.get_statements(agents=[term]).statements
    stmts_json = stmts_to_json(stmts)
    valid_stmts = set()
    if source_apis:
        idx = 0
        for stmt in stmts_json:
            evidences = stmt.get("evidence", [])
            for ev in evidences:
                if ev["source_api"] in source_apis:
                    valid_stmts.add(stmts[idx])
            idx += 1
        return len(valid_stmts)
    return len(stmts)


"""
Extracts information from XML

Parameters
----------
fileContent : 
    XML Content for the journal
citationCount : 
    Citation count for the PMID
term:
    Reactome query term
"""
def extractFromXML(pmid,  term):

    flag = True
    while flag:
        try:
            xmlContent = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="+pmid)
            flag = False
        except Exception as e:
            time.sleep(.5)

    fileContent = xmlContent.text
    destFileName = "eutils_output.tsv"
    if(os.path.isfile(destFileName)):
        destCSV = open(destFileName, 'a')
    else:
        destCSV = open(destFileName, 'w')
        print('\t'.join(["PMID", "TERM", "JOURNAL_TITLE", "YEAR", "PMCID", "DOI", "PMC_CITATION_COUNT",
                         "INDRA_STATEMENT_COUNT", "OC_CITATION_COUNT", "INDRA_QUERY_TERM_STATEMENT_COUNT", "PMID_COUNT"]), file=destCSV)
    writer = csv.writer(destCSV, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    tree = ET.fromstring(fileContent, ET.XMLParser(encoding='utf-8'))
    pm_articles = tree.findall('./PubmedArticle')
    citation_count = citationCount(pmid)
    for art_ix, pm_article in enumerate(pm_articles):
        medline_citation = pm_article.find('./MedlineCitation')
        pubmed = pm_article.find('./PubmedData')
        try:
            history_pub_date = pubmed.find(
                './History/PubMedPubDate[@PubStatus="pubmed"]')
            year = parser._find_elem_text(history_pub_date, 'Year')
            PublicationTypeList = medline_citation.find(
                './Article/PublicationTypeList')
            pubType = parser._find_elem_text(
                PublicationTypeList, 'PublicationType')
            topics = []
            for topic in medline_citation.findall('./MeshHeadingList/MeshHeading'):
                topics.append(topic.find('DescriptorName').text)
            topics_string = ' , '.join(topics)
        except Exception as err:
            print("Err: EUtils:", err)
            continue

        pub_year = None if (year is None) else int(year)
        article_info = parser._get_article_info(
            medline_citation, pm_article.find('PubmedData'))
        journal_info = parser._get_journal_info(medline_citation, False)

        # Preparing results
        title = journal_info["journal_abbrev"] or ""
        Year = pub_year
        DOI = article_info["doi"] or ""
        PMCID = article_info["pmcid"] or ""
        PMID = article_info["pmid"] or ""
        pmc_citation_count = citation_count
        OC_CITATION_COUNT = 0
        try:
            if DOI != "":
                output = requests.get(
                    "https://opencitations.net/api/v1/metadata/" + DOI).json()
                if len(output) > 0:
                    OC_CITATION_COUNT = output[0]["citation_count"]
        except:
            pass
        stmt = indra_db_rest.get_statements_for_paper(
            [('pmid', PMID)]).statements
        indra_stmt_count = len(stmt)
        # storing in tsv file
        writer.writerow([PMID, term, title, Year, PMCID, DOI, pmc_citation_count,
                         indra_stmt_count, OC_CITATION_COUNT,  getIndraQueryTermStmtCount(term)])
    # Closing file
    destCSV.close()


"""
Generate a TSV containing meta details of PMID from EUtils
"""
def getEUtilsInfo():
    with open("pmid_list.txt") as file:
        for line in file:
            try:
                line = line.strip().split("~")
                pmid = line[0]
                term = line[1]

                extractFromXML(pmid, term)
            except Exception as e:
                print("Err: EUtils: ", e, line)
