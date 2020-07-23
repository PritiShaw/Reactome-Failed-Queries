Reactome Failed Searches Analysis
---

## Steps to Run

1. **Get PMID list for Reactome Failed Searches**  
    ```sh
    python getPMID.py
    ```
    Input: [Reactome Failed Search terms](https://raw.githubusercontent.com/cannin/reach-query/master/queries.csv)  
    Output: `pmid_list.txt`

2. **Get Journal Details from EUtils**
    ```sh
    python getEUtilsInfo.py
    ```
    Input: `pmid_list.txt`  
    Output: `eutils_output.csv`

3. **Get Abstracts from PMIDs**
    ```sh
    python getAbstracts.py
    ```
    Input: `pmid_list.txt`  
    Output: `abstracts.txt`

4. **Get MESH Terms for the abstracts**  
    Upload `abstracts.txt` in [Batch Medical Text Indexer (MTI)](https://ii.nlm.nih.gov/Batch/UTS_Required/mti.shtml) for batch processing. You might have to make an account, which can be done [here](https://uts.nlm.nih.gov/license.html).  
    You will me notified in mail when processing is done.
    Download the `text.out` file and note the path to it, this will be input to our next step.

5. **Merge Journal Details and Extracted MESH terms**
    ```sh
    python mergeOutputs.py PATH_TO_STEP_2_output PATH_TO_STEP_3_output
    ```
    Input: Output of Step 2 and 4  
    Output: `final_output.tsv`

## Results
Final Result : [final_output.tsv](/outputs/final_output.tsv)  
Stepwise Outputs are present in [outputs](/outputs) directory
