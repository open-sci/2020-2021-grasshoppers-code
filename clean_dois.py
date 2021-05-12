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

from __future__ import annotations

import re, csv
from collections import defaultdict
from itertools import product, islice
from tqdm import tqdm
from support import Support

class Clean_DOIs(object):
    def __init__(self, crossref_dois:list=list(), request_cache:str="", logs:dict={}):
        self.crossref_dois = crossref_dois
        if len(self.crossref_dois) > 0:
            print("[Clean_DOIs: INFO] Storing Crossref DOIs in a set")
            self.crossref_dois = {item["crossref_doi"].lower() for item in crossref_dois}
        self.request_cache = request_cache
        self.logs = logs
        prefix_dx = r"HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/"
        prefix_doi = r"HTTPS:\/\/D[0|O]I\.[0|O]RG\/"
        suffix_dcsupplemental = r"\/-\/DCSUPPLEMENTAL"
        suffix_suppinfo = r"SUPPINF[0|O](\.)?"
        suffix_pmid1 = r"[\.|\(|,|;]?PMID:\d+.*?"
        suffix_pmid2 = r"[\.|\(|,|;]?PMCID:PMC\d+.*?"
        suffix_epub = r"[\(|\[]EPUBAHEADOFPRINT[\)\]]"
        suffix_published_online = r"[\.|\(|,|;]?ARTICLEPUBLISHEDONLINE.*?\d{4}"
        suffix_http = r"[\.|\(|,|;]*HTTP:\/\/.*?"
        suffix_subcontent = r"\/(META|ABSTRACT|FULL|EPDF|PDF|SUMMARY)([>|\)](LAST)?ACCESSED\d+)?"
        suffix_accessed = r"[>|\)](LAST)?ACCESSED\d+"
        suffix_sagepub = r"[\.|\(|,|;]?[A-Z]*\.?SAGEPUB.*?"
        suffix_dotted_line = r"\.{5}.*?"
        suffix_delimiters = r"[\.|,|<|&|\(|;]+"
        suffix_doi_mark = r"\[DOI\].*?"
        suffix_year = r"\(\d{4}\)?"
        suffix_query = r"\?.*?=.*?"
        suffix_hash = r"#.*?"
        self.suffix_regex_lst = [suffix_dcsupplemental, suffix_suppinfo, suffix_pmid1, suffix_pmid2, suffix_epub,
                            suffix_published_online, suffix_http, suffix_subcontent, suffix_accessed, suffix_sagepub,
                            suffix_dotted_line, suffix_delimiters, suffix_doi_mark, suffix_year,
                            suffix_query, suffix_hash]
        self.prefix_regex_lst = [prefix_dx, prefix_doi]
        self.prefix_regex = r"(.*?)(?:\.)?(?:" + "|".join(self.prefix_regex_lst) + r")(.*)"
        self.suffix_regex = r"(.*?)(?:" + "|".join(self.suffix_regex_lst) + r")$"

    def check_dois_validity(self, data:list, autosave_path:str="", cache_every:int=100) -> list:
        if autosave_path != "":
            start_index, checked_dois = Support.read_cache(autosave_path=autosave_path)
            pbar = tqdm(total=len(data)-start_index)
            data = islice(data, start_index + 1, None)
        else:
            checked_dois = list()
            pbar = tqdm(total=len(data))
        i = 0
        for row in data:
            if autosave_path != "" and i == cache_every:
                Support.dump_csv(data=checked_dois, path=autosave_path)
                i = 0
            valid_citing_doi = row["Valid_citing_DOI"].lower()
            invalid_cited_doi = row["Invalid_cited_DOI"].lower()
            invalid_dictionary = {
                "Valid_citing_DOI": valid_citing_doi,
                "Invalid_cited_DOI": invalid_cited_doi, 
                "Valid_DOI": "",
                "Already_valid": 0
            }
            if invalid_cited_doi in self.crossref_dois:
                handle = {"responseCode": 1}
            else:
                handle = Support().handle_request(url=f"https://doi.org/api/handles/{invalid_cited_doi}", cache_path=self.request_cache, error_log_dict=self.logs)
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
            i += 1             
            pbar.update(1)
        pbar.close()
        return checked_dois
    
    def procedure(self, data:list, autosave_path:str="", cache_every:int=100) -> list:
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
            valid_citing_doi = row["Valid_citing_DOI"].lower()
            invalid_cited_doi = row["Invalid_cited_DOI"].lower()
            already_valid = row["Already_valid"]
            unclean_dictionary = {
                "Valid_citing_DOI": valid_citing_doi,
                "Invalid_cited_DOI": invalid_cited_doi,
                "Valid_DOI": row["Valid_DOI"].lower(),
                "Already_valid": already_valid,
                "Prefix_error": 0,
                "Suffix_error": 0,
                "Other-type_error": 0
            }
            if int(already_valid) == 0:
                new_doi, classes_of_errors = self.clean_doi(invalid_cited_doi)
                new_doi = new_doi.lower()
                clean_dictionary = {
                    "Valid_citing_DOI": valid_citing_doi,
                    "Invalid_cited_DOI": invalid_cited_doi,
                    "Valid_DOI": new_doi,
                    "Already_valid": already_valid,
                    "Prefix_error": classes_of_errors["prefix"],
                    "Suffix_error": classes_of_errors["suffix"],
                    "Other-type_error": classes_of_errors["other-type"]
                }
                if new_doi != invalid_cited_doi:
                    if new_doi in self.crossref_dois:
                        handle = {"responseCode": 1}
                    else:
                        handle = Support().handle_request(url=f"https://doi.org/api/handles/{new_doi}", cache_path=self.request_cache, error_log_dict=self.logs)
                    if handle is not None:
                        if handle["responseCode"] == 1:
                            output.append(clean_dictionary)
                        else:
                            output.append(unclean_dictionary)
                    else:
                        output.append(unclean_dictionary)
                elif new_doi == invalid_cited_doi:
                    output.append(unclean_dictionary)
            elif int(already_valid) == 1:
                output.append(unclean_dictionary)
            pbar.update(1)
            i += 1
        pbar.close()
        return output
    
    def clean_doi(self, doi:str) -> tuple[str, dict]:
        tmp_doi = doi.replace(" ", "")
        prefix_match = re.search(self.prefix_regex, tmp_doi, re.IGNORECASE)
        classes_of_errors = {
            "prefix": 0,
            "suffix": 0,
            "other-type": 0
        }
        if prefix_match:
            tmp_doi = prefix_match.group(1)
            classes_of_errors["prefix"] = 1
        suffix_match = re.search(self.suffix_regex, tmp_doi, re.IGNORECASE)
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




        
    
    

          


        