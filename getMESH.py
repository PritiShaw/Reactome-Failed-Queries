import requests
import os

from urllib.request import urlopen
from xml.etree.ElementTree import parse


def getAbstracts():
    with open("pmid_list.txt") as file:
        with open('abstract.txt', 'w') as o:
            for inp in file:
                pmid = inp.strip().split("~")[0]
                var_url = urlopen(
                    f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pmid}')
                xmldoc = parse(var_url)
                for item in xmldoc.iterfind('PubmedArticle'):
                    try:
                        abstract_text = item.findtext(
                            'MedlineCitation/Article/Abstract/AbstractText')
                        article_title = item.findtext(
                            'MedlineCitation/Article/ArticleTitle')
                        if abstract_text:
                            print('UI  - ', pmid, file=o)
                            print(
                                'TI  - ', article_title.encode("ascii", "ignore"), file=o)
                            print(
                                'AB  - ', abstract_text.encode("ascii", "ignore"), file=o)
                            print("\n", file=o)
                        else:
                            print("Err: ", "Undefined Abstract")
                    except Exception as e:
                        print("Err: ", e)

def getMESH():
    getAbstracts()
    os.system("bash handleMTI.sh >> mesh.txt")
    