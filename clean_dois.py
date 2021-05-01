import re
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
        self.prefix_regex = "(.*?)(?:\.)?(?:HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/|HTTPS:\/\/D[0|O]I\.[0|O]RG\/)(.*)"
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
        suffix_double_doi = "[\.|\(|,|;]10.\d{4}\/.*?"
        suffix_doi_mark = "\[DOI\].*?"
        suffix_year = "\(\d{4}\)?"
        suffix_query = "\?.*?=.*?"
        suffix_hash = "#.*?"
        suffix_regex_lst = [suffix_dcsupplemental, suffix_suppinfo, suffix_pmid1, suffix_pmid2, suffix_epub,
                            suffix_published_online, suffix_http, suffix_subcontent, suffix_accessed, suffix_sagepub,
                            suffix_dotted_line, suffix_delimiters, suffix_double_doi, suffix_doi_mark, suffix_year,
                            suffix_query, suffix_hash]
        self.suffix_regex = "(.*?)(?:" + "|".join(suffix_regex_lst) + ")$"

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



        
    
    

          


        