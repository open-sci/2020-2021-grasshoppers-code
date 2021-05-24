from typing import Tuple

from support import Support
import re
from tqdm import tqdm
from itertools import islice

doi_logs = dict()

def clean_doi(doi:str) -> Tuple[str, dict]:
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


def procedure(data:list, autosave_path:str="", cache_every:int=100) -> list:
    if autosave_path != "":
        start_index, output = Support.read_cache(autosave_path=autosave_path)
        pbar = tqdm(total=len(data)-start_index)
        data = islice(data, start_index + 1, None)
    else:
        output = list()
        pbar = tqdm(total=len(data))
    i = 0
    for row in data:
        if autosave_path != "" and i == cache_every:
            Support.dump_csv(data=output, path=autosave_path)
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

def remove_already_valid(data:list, path_already_valid:str) -> list:
    already_valid = Support.process_csv_input(path=path_already_valid)
    already_valid_dois = set()
    output = list()
    for row in already_valid:
        if row["Already_valid"] == "1":
            already_valid_dois.add(row["Valid_DOI"])
    for row in data:
        if row["Invalid_cited_DOI"] in already_valid_dois and len(row["Valid_DOI"]) > 0:
            output.append({
                "Invalid_cited_DOI": row["Invalid_cited_DOI"],
                "Valid_DOI": "",
                "Prefix_error": 0,
                "Suffix_error": 0,
                "Other-type_error": 0
            })
        else:
            output.append(row)
    return output

# data = Support.process_csv_input(path="./dataset/invalid_dois.csv")
# output = procedure(data=data, autosave_path="./cache/xu_2019_results.csv", cache_every=10000)
output = Support.process_csv_input(path="./output/xu_2019_results.csv")
output = remove_already_valid(data=output, path_already_valid="./output/checked_dois.csv")
# Support().dump_csv(data=output, path="./output/xu_2019_results_no_already_valid.csv")
# if len(doi_logs) > 0:
#     print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
#     Support().dump_json(doi_logs, "./doi_logs.json")




