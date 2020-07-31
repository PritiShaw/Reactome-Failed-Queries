import requests
import multiprocessing
import os
import datetime

from tqdm import tqdm_notebook as tqdm


from getEUtilsInfo import getEUtilsInfo
from getMESH import getMESH
from getPMID import getPMID
from mergeOutputs import mergeOutputs

history_file_path = "/src/processor/history"


def saveInHistory(terms):
    """
    Save processed terms in file

    Parameters
    ----------
    terms:  []
        List of processed terms
    """
    with open(history_file_path, "a") as out_file:
        out_file.write('\n'.join(terms)+'\n')


if __name__ == "__main__":
    history = set()

    if os.path.isfile(history_file_path):
        with open(history_file_path, "r") as history_file:
            for line in history_file:
                history.add(line.strip())

    terms = [[]]

    terms_request = requests.get(
        "https://gist.githubusercontent.com/PritiShaw/03ce10747835390ec8a755fed9ea813d/raw/cc72cb5479f09b574e03ed22c8d4e3147e09aa0c/Reactome.csv")
    inp_terms = terms_request.text.splitlines()

    for term in inp_terms[1:6]:
        term_parts = term.split(",")
        if len(term_parts) == 2 and int(term_parts[1]) > 9 and term not in history:
            terms[-1].append(term)
            if len(terms[-1]) == 10:
                terms.append([])

    for chunk in tqdm(terms):
        getPMID(chunk)
        process_mesh = multiprocessing.Process(target=getMESH)
        process_meta = multiprocessing.Process(target=getEUtilsInfo)

        process_meta.start()
        process_mesh.start()
        process_meta.join()
        process_mesh.join()

        mergeOutputs("eutils_output.tsv", "mesh.txt", "/src/processor")
        history.update(chunk)
        saveInHistory(chunk)
        os.system("rm eutils_output.csv abstract.txt mesh.txt pmid_list.txt")
