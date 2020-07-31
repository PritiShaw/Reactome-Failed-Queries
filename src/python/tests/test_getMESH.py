import sys, os
sys.path.append('../')

from getMESH import getAbstracts

def test_extractListID():
    with open("pmid_list.txt", "w") as file:
        file.write("32674038~DMRT1\n32628996~DMRT1\n32590948~DMRT1\n32497821~DMRT1\n32447491~DMRT1\n")
    getAbstracts()
    assert os.path.exists("abstract.txt")

