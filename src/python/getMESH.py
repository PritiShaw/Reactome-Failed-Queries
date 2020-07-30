# getMESH.py
from xml.etree.ElementTree import parse
from urllib.request import urlopen
import time
import os
import requests
from jnius import autoclass
import jnius_config
jnius_config.add_classpath("./lib/*")


GenericBatchNew = autoclass("GenericBatchNew")


def getAbstracts(abstract_filepath):
    """
    Get abstracts from PMID and generate input file for MESH Batch processing
    """
    with open("pmid_list.txt") as file:
        with open(abstract_filepath, 'wb') as o:
            for inp in file:
                pmid = inp.strip().split("~")[0]
                flag = True
                while flag:
                    try:
                        var_url = urlopen(
                            f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pmid}')
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
    abstract_filepath = 'abstract.txt'
    getAbstracts(abstract_filepath)

    email_id = os.environ['MTI_EMAIL_ID']
    username = os.environ['MTI_USERNAME']
    password = os.environ['MTI_PASSWORD']

    batch = GenericBatchNew()
    result = batch.processor(
        ["--email", email_id, abstract_filepath], username, password)
        
    with open("mesh.txt", "w") as op_file:
        op_file.write(result)
