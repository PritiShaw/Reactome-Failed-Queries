import requests
import multiprocessing
import os

from tqdm import tqdm
from getPMID import getPMID
from getMESH import getMESH
from getEUtilsInfo import getEUtilsInfo
from mergeOutputs import mergeOutputs


def saveInHistory(terms):
    with open("./processor/history", "a") as out_file:
        out_file.write('\n'.join(terms))


if __name__ == "__main__":
    terms_request = requests.get(
        "https://raw.githubusercontent.com/cannin/reach-query/master/queries.csv")
    inp_terms = terms_request.text.splitlines()
    history = set()
    with open("./processor/history","w+") as history_file:
        for line in history_file:
            history.add(line.trim())
    terms = [[]]
    for term in inp_terms[1:]:
        if term not in history:
            terms[-1].append(term)
            if len(terms[-1])==5:
                terms.append([])

    for chunk in tqdm(terms):
        getPMID(chunk)
        process_mesh = multiprocessing.Process(target=getMESH)
        process_meta = multiprocessing.Process(target=getEUtilsInfo)

        process_meta.start()
        process_mesh.start()
        process_meta.join()
        process_mesh.join()

        mergeOutputs("eutils_output.csv","mesh.txt","./processor")
        history.update(chunk)        
        saveInHistory(chunk)
        os.system("bash handleGit.sh")
        os.system("bash cleanup.sh")
