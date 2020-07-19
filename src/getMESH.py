import requests
import os
import time

from urllib.request import urlopen
from xml.etree.ElementTree import parse

"""
Get abstracts from PMID and generate input file for MESH Batch processing
"""
def getAbstracts():
    with open("pmid_list.txt") as file:
        with open('abstract.txt', 'w') as o:
            for inp in file:
                pmid = inp.strip().split("~")[0]
                flag = True
                while flag:
                    try:
                        var_url = urlopen(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pmid}')
                        flag = False
                    except:
                        time.sleep(.5)
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
                            print("Err: MESH: ", "Undefined Abstract")
                    except Exception as e:
                        print("Err: MESH: ", e)

def getMESH():
    getAbstracts()
    os.system("bash handleMTI.sh >> mesh.txt")
    