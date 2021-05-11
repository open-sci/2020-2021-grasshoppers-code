from __future__ import annotations

from support import Support
import re
from tqdm import tqdm
from itertools import islice

doi_logs = dict()

def clean_doi(doi):
    prefix_regex = "^(?:D[0|O]I\/?|HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/|[0|O]RG\/|[:\/]|\d+\.HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/?)+(.*)"
    suffix_regex = "(.*?)(?:\/-\/DCSUPPLEMENTAL|\/SUPPINF[0|O]\.?|[\s\.;]?PMID:[\d]+|[\.\/:]|[\s\.;]?PMCID:PMC\d+|[\(\.;]EPUB|[\(\[]EPUBAHEADOFPRINT[\)\]]|[\s\.;]?ARTICLEPUBLISHEDONLINE.*?\d{4}|[\.\(]*HTTP:\/\/.*?)$"
    tmp_doi = doi.replace(" ", "")
    prefix_match = re.search(prefix_regex, tmp_doi, re.IGNORECASE)
    classes_of_errors = {
        "prefix": 0,
        "suffix": 0,
        "other-type": 0
    }
    if prefix_match:
        tmp_doi = prefix_match.group(1)
        classes_of_errors["prefix"] = 1
    suffix_match = re.search(suffix_regex, tmp_doi, re.IGNORECASE)
    if suffix_match:
        tmp_doi = suffix_match.group(1)
        classes_of_errors["suffix"] = 1
    new_doi = re.sub("\\\\", "", tmp_doi)
    new_doi = re.sub("__", "_", new_doi)
    new_doi = re.sub("\\.\\.", ".", new_doi)
    new_doi = re.sub("<.*?>.*?</.*?>", "", new_doi)
    new_doi = re.sub("<.*?/>", "", new_doi)
    if new_doi != tmp_doi:
        classes_of_errors["other-type"] = 1
    return new_doi, classes_of_errors


def procedure(data, cache_path:str, cache_every:int=100):
    start_index, output = Support.read_cache(cache_path=cache_path)
    pbar = tqdm(total=len(data)-start_index)
    data = islice(data, start_index + 1, None)
    i = 0
    for row in data:
        if i == cache_every:
            Support.dump_csv(data=output, path=cache_path)
            i = 0
        invalid_cited_doi = row["Invalid_cited_DOI"].lower()
        unclean_dictionary = {
            "Invalid_cited_DOI": invalid_cited_doi,
            "Valid_DOI": "",
            "Prefix_error": 0,
            "Suffix_error": 0,
            "Other-type_error": 0
        }
        new_doi, classes_of_errors = clean_doi(invalid_cited_doi)
        new_doi = new_doi.lower()
        clean_dictionary = {
            "Invalid_cited_DOI": invalid_cited_doi,
            "Valid_DOI": new_doi,
            "Prefix_error": classes_of_errors["prefix"],
            "Suffix_error": classes_of_errors["suffix"],
            "Other-type_error": classes_of_errors["other-type"]
        }
        if new_doi != invalid_cited_doi and new_doi != "":
            handle = Support().handle_request(url=f"https://doi.org/api/handles/{new_doi}", cache_path="",
                                              error_log_dict=doi_logs)
            if handle is not None:
                if handle["responseCode"] == 1:
                    output.append(clean_dictionary)
                else:
                    output.append(unclean_dictionary)
            else:
                output.append(unclean_dictionary)
        else:
            output.append(unclean_dictionary)
        pbar.update(1)
        i += 1
    pbar.close()
    return output

data = Support.process_csv_input(path="./dataset/invalid_dois.csv")
output = procedure(data=data, cache_path="./cache/xu_2019_results.csv")
Support().dump_csv(data=output, path="./xu_2019_results.csv")
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
    Support().dump_json(doi_logs, "./doi_logs.json")




