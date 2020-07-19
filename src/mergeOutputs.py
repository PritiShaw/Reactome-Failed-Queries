import csv
import json
import sys
import os

"""
Merge outputs from EUtils and MESH terms from 

Parameters
----------
path_eutils:
    Path to TSV file containing metadata from EUtils
path_mesh:
    Path to MESH terms extracted by Web API
path_output_dir:
    Path to Output directory
"""
def mergeOutputs(path_eutils, path_mesh, path_output_dir):
    details = {}

    with open(path_eutils) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row["PMID"] not in details:
                details[row["PMID"]] = {}
            details[row["PMID"]][row["TERM"]] = {
                "journal": row["JOURNAL_TITLE"],
                "year": row["YEAR"],
                "pmc": row["PMCID"],
                "doi": row["DOI"],
                "citation_count": row["PMC_CITATION_COUNT"],
                "indra_stmt_count": row["INDRA_STATEMENT_COUNT"],
                "oc_citation_count": row["OC_CITATION_COUNT"],
                "indra_query_term_stmt_count": row["INDRA_QUERY_TERM_STATEMENT_COUNT"],
                "mesh": []
            }

    with open(path_mesh) as mesh:
        for line in mesh:
            inp = line.split("|")
            mesh_term = inp[1]
            pmid = inp[0]
            for term in details[pmid]:
                details[pmid][term]["mesh"].append(mesh_term)

    with open(os.path.join(path_output_dir, "output.tsv"), 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
        writer.writerow(["QUERY_TERM", "PMID", "JOURNAL_TITLE", "YEAR", "PMCID",
                         "DOI", "PMC_CITATION_COUNT", "INDRA_STATEMENT_COUNT", "OC_CITATION_COUNT", "INDRA_QUERY_TERM_STATEMENT_COUNT", "MESH_TERMS"])
        for key in details:
            for term in details[key]:
                writer.writerow([term, key, details[key][term]["journal"], details[key][term]["year"], details[key][term]["pmc"], details[key][term]
                                 ["doi"], details[key][term]["citation_count"], details[key][term][
                    "indra_stmt_count"], details[key][term]["oc_citation_count"],
                    details[key][term]["indra_query_term_stmt_count"], "|".join(details[key][term]["mesh"])])
