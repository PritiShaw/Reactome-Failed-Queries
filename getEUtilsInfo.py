import os
import gzip
import time
import sys
import csv
import requests
import indra.literature.pubmed_client as parser
import xml.etree.ElementTree as ET
from indra.sources import indra_db_rest
from indra.assemblers.html.assembler import HtmlAssembler

os.environ["INDRA_DB_REST_URL"] = "API_ENDPOINT"
start_time = time.time()


def extractFromXML(fileContent, citationCount, term):
    destFileName = "eutils_output.csv"
    if(os.path.isfile(destFileName)):
        destCSV = open(destFileName, 'a')
    else:
        destCSV = open(destFileName, 'w')
        print("PMID,TERM,JOURNAL_TITLE,YEAR,PMCID,DOI,PMC_CITATION_COUNT,INDRA_STATEMENT_COUNT", file=destCSV)
    writer = csv.writer(destCSV, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    tree = ET.fromstring(fileContent, ET.XMLParser(encoding='utf-8'))
    pm_articles = tree.findall('./PubmedArticle')
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
            print(err)
            continue
        # Add the Publication date from Journal info

        pub_year = None if (year is None) else int(year)

        # Get article info
        article_info = parser._get_article_info(
            medline_citation, pm_article.find('PubmedData'))
        # Get journal info
        journal_info = parser._get_journal_info(medline_citation, False)

        # Preparing results
        title = journal_info["journal_abbrev"] or ""
        Year = pub_year
        DOI = article_info["doi"] or ""
        PMCID = article_info["pmcid"] or ""
        PMID = article_info["pmid"] or ""
        article_type = pubType or ""
        article_topics = topics_string or ""
        pmc_citation_count = citationCount

        stmt = indra_db_rest.get_statements_for_paper(
            [('pmid', PMID)]).statements
        # print(citationCount,stmt)
        indra_stmt_count = len(stmt)
        # storing in csv file
        writer.writerow([PMID, term, title, Year, PMCID, DOI,
                         pmc_citation_count, indra_stmt_count])
    # Closing file
    destCSV.close()


def citationCount(fileContent):
    tree = ET.fromstring(fileContent, ET.XMLParser(encoding='utf-8'))
    ID = tree.findall('./LinkSet/LinkSetDb/Link')
    return len(ID)


with open("pmid_list.txt") as f:
    for line in f:
        try:
            line = line.strip().split("~")
            pmid = line[0]
            term = line[1]
            flag = True
            while flag:
                try:
                    citationCount_url = requests.get(
                        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&id="+pmid)
                    flag = False
                except Exception as e:
                    time.sleep(.5)

            count = citationCount(citationCount_url.text)

            flag = True
            while flag:
                try:
                    xmlContent = requests.get(
                        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="+pmid)
                    flag = False
                except Exception as e:
                    time.sleep(.5)

            extractFromXML(xmlContent.text, count, term)
        except Exception as e:
            print("Err: ", e, line)
