# ISC License (ISC)
# ==================================
# Copyright 2021 Arcangelo Massari, Cristian Santini, Ricarda Boente, Deniz Tural

# Permission to use, copy, modify, and/or distribute this software for any purpose with or
# without fee is hereby granted, provided that the above copyright notice and this permission
# notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import re
from collections import defaultdict
from itertools import product
from tqdm import tqdm
from support import Support

class Clean_DOIs(object):
    def __init__(self, crossref_dois:list=list(), cache_path:str="", logs:dict={}):
        self.crossref_dois = crossref_dois
        if len(self.crossref_dois) > 0:
            print("[Clean_DOIs: INFO] Storing Crossref DOIs in a set")
            self.crossref_dois = {item["crossref_doi"] for item in crossref_dois}
        self.cache_path = cache_path
        self.logs = logs
        prefix_dx = "HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/"
        prefix_doi = "HTTPS:\/\/D[0|O]I\.[0|O]RG\/"
        suffix_dcsupplemental = "\/-\/DCSUPPLEMENTAL"
        suffix_suppinfo = "SUPPINF[0|O](\.)?"
        suffix_pmid1 = "[\.|\(|,|;]?PMID:\d+.*?"
        suffix_pmid2 = "[\.|\(|,|;]?PMCID:PMC\d+.*?"
        suffix_epub = "[\(|\[]EPUBAHEADOFPRINT[\)\]]"
        suffix_published_online = "[\.|\(|,|;]?ARTICLEPUBLISHEDONLINE.*?\d{4}"
        suffix_http = "[\.|\(|,|;]*HTTP:\/\/.*?"
        suffix_subcontent = "\/(META|ABSTRACT|FULL|EPDF|PDF|SUMMARY)([>|\)](LAST)?ACCESSED\d+)?"
        suffix_accessed = "[>|\)](LAST)?ACCESSED\d+"
        suffix_sagepub = "[\.|\(|,|;]?[A-Z]*\.?SAGEPUB.*?"
        suffix_dotted_line = "\.{5}.*?"
        suffix_delimiters = "[\.|,|<|&|\(|;]+"
        suffix_doi_mark = "\[DOI\].*?"
        suffix_year = "\(\d{4}\)?"
        suffix_query = "\?.*?=.*?"
        suffix_hash = "#.*?"
        self.suffix_regex_lst = [suffix_dcsupplemental, suffix_suppinfo, suffix_pmid1, suffix_pmid2, suffix_epub,
                            suffix_published_online, suffix_http, suffix_subcontent, suffix_accessed, suffix_sagepub,
                            suffix_dotted_line, suffix_delimiters, suffix_doi_mark, suffix_year,
                            suffix_query, suffix_hash]
        self.prefix_regex_lst = [prefix_dx, prefix_doi]
        self.prefix_regex = "(.*?)(?:\.)?(?:" + "|".join(self.prefix_regex_lst) + ")(.*)"
        self.suffix_regex = "(.*?)(?:" + "|".join(self.suffix_regex_lst) + ")$"

    def check_dois_validity(self, data:list) -> list:
        checked_dois = list()
        pbar = tqdm(total=len(data))
        for row in data:
            valid_citing_doi = row["Valid_citing_DOI"]
            invalid_cited_doi = row["Invalid_cited_DOI"]
            invalid_dictionary = {
                "Valid_citing_DOI": valid_citing_doi,
                "Invalid_cited_DOI": invalid_cited_doi, 
                "Valid_DOI": "",
                "Already_valid": 0
            }
            if invalid_cited_doi in self.crossref_dois:
                handle = {"responseCode": 1}
            else:
                handle = Support().handle_request(url=f"https://doi.org/api/handles/{invalid_cited_doi}", cache_path=self.cache_path, error_log_dict=self.logs)
            if handle is not None:
                if handle["responseCode"] == 1:
                    checked_dois.append(
                        {"Valid_citing_DOI": valid_citing_doi,
                        "Invalid_cited_DOI": invalid_cited_doi, 
                        "Valid_DOI": invalid_cited_doi,
                        "Already_valid": 1
                        })
                else:
                    checked_dois.append(invalid_dictionary)       
            else:
                checked_dois.append(invalid_dictionary)             
            pbar.update(1)
        pbar.close()
        return checked_dois
    
    def procedure(self, data:list) -> list:
        output = list()
        pbar = tqdm(total=len(data))
        for row in data:
            valid_citing_doi = row["Valid_citing_DOI"]
            invalid_cited_doi = row["Invalid_cited_DOI"]
            unclean_dictionary = {
                "Valid_citing_DOI": valid_citing_doi,
                "Invalid_cited_DOI": invalid_cited_doi,
                "Valid_DOI": row["Valid_DOI"],
                "Already_valid": row["Already_valid"],
                "Prefix_error": 0,
                "Suffix_error": 0,
                "Other-type_error": 0
            }
            if row["Already_valid"] != 1:
                new_doi, classes_of_errors = self.clean_doi(invalid_cited_doi)
                clean_dictionary = {
                    "Valid_citing_DOI": valid_citing_doi,
                    "Invalid_cited_DOI": invalid_cited_doi,
                    "Valid_DOI": new_doi,
                    "Already_valid": row["Already_valid"],
                    "Prefix_error": classes_of_errors["prefix"],
                    "Suffix_error": classes_of_errors["suffix"],
                    "Other-type_error": classes_of_errors["other-type"]
                }
                if new_doi != invalid_cited_doi:
                    if new_doi in self.crossref_dois:
                        handle = {"responseCode": 1}
                    else:
                        handle = Support().handle_request(url=f"https://doi.org/api/handles/{new_doi}", cache_path=self.cache_path, error_log_dict=self.logs)
                    if handle is not None:
                        if handle["responseCode"] == 1:
                            output.append(clean_dictionary)
                        else:
                            output.append(unclean_dictionary)
                    else:
                        output.append(unclean_dictionary)
                else:
                    output.append(unclean_dictionary)
            else:
                output.append(unclean_dictionary)
            pbar.update(1)
        pbar.close()
        return output
    
    def clean_doi(self, doi:str) -> str:
        tmp_doi = doi.upper().replace(" ", "")
        prefix_match = re.search(self.prefix_regex, tmp_doi)
        classes_of_errors = {
            "prefix": 0,
            "suffix": 0,
            "other-type": 0
        }
        if prefix_match:
            tmp_doi = prefix_match.group(1)
            classes_of_errors["prefix"] += 1
        suffix_match = re.search(self.suffix_regex, tmp_doi)
        if suffix_match:
            tmp_doi = suffix_match.group(1)
            classes_of_errors["suffix"] += 1
        new_doi = re.sub("\\\\", "", tmp_doi)
        new_doi = re.sub("__", "_", tmp_doi)
        new_doi = re.sub("\\.\\.", ".", tmp_doi)
        new_doi = re.sub("<.*?>.*?</.*?>", "", tmp_doi)
        new_doi = re.sub("<.*?/>", "", tmp_doi)
        if new_doi != tmp_doi:
            classes_of_errors["other-type"] += 1
        return new_doi, classes_of_errors
    
    def get_number_of_matches(self, data:list) -> dict:
        classes_of_errors = {
            "other-type": {
                "\\\\": 0,
                "__": 0,
                "\\.\\.": 0,
                "<.*?>.*?</.*?>": 0,
                "<.*?/>": 0
            }
        }
        for regex in self.prefix_regex_lst:
            classes_of_errors.setdefault("prefix", dict())
            classes_of_errors["prefix"].setdefault(regex, 0)
        for regex in self.suffix_regex_lst:
            classes_of_errors.setdefault("suffix", dict())
            classes_of_errors["suffix"].setdefault(regex, 0)
        pbar = tqdm(total=3)
        for category in classes_of_errors:
            print(f"[Clean_DOIs:INFO] Checking matches for class {category}")
            for regex in classes_of_errors[category]:
                for row in data:
                    doi = row["Invalid_cited_DOI"].upper()
                    match = re.search(regex, doi)
                    if match:
                        classes_of_errors[category][regex] += 1
            pbar.update(1)
        pbar.close()
        return classes_of_errors




        
    
    

          


        