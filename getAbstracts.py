import requests
from urllib.request import urlopen
from xml.etree.ElementTree import parse

f = open("pmid_list.txt")
with open('abstract.txts','w') as o:
    for i in f:
        pmid = i.strip().split("~")[0]
        var_url = urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={}'.format(pmid))
        xmldoc = parse(var_url)
        for item in xmldoc.iterfind('PubmedArticle'):
            try:
                abstract_text = item.findtext('MedlineCitation/Article/Abstract/AbstractText')
                article_title = item.findtext('MedlineCitation/Article/ArticleTitle')
                if abstract_text:
                  print('UI  - ', pmid, file=o)
                  print('TI  - ', article_title.encode("ascii","ignore"), file=o)
                  print('AB  - ', abstract_text.encode("ascii","ignore"), file=o)
                  print("\n", file=o)
                else:
                  print("Err: ", "Undefined Abstract")    
            except Exception as e:
                print("Err: ", e)  
f.close()