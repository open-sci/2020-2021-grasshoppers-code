import re
from tqdm import tqdm
from support import Support

class Clean_DOIs(object):
    def __init__(self):
        self.prefix_regex = "(.*?)(?:\.)?(?:HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/|HTTPS:\/\/D[0|O]I\.[0|O]RG\/)(.*)"
        self.year_regex = "(.*?)(\(\d{4}\)?)$"
        suffix_regex1 = "\/-\/DCSUPPLEMENTAL"
        suffix_regex2 = "SUPPINF[0|O](\.)?"
        suffix_regex3 = "[\.|(|,|;]?PMID:\d+.*?"
        suffix_regex4 = "[\.|(|,|;]?PMCID:PMC\d+.*?"
        suffix_regex5 = "[(|\[]EPUBAHEADOFPRINT[)\]]"
        suffix_regex6 = "[\.|(|,|;]?ARTICLEPUBLISHEDONLINE.*?\d{4}"
        suffix_regex7 = "[\.|(|,|;]*HTTP:\/\/.*?"
        suffix_regex8 = "[\.\/](META|ABSTRACT|FULL|EPDF|PDF|SUMMARY)>?"
        suffix_regex9 = "([\/\.](META|ABSTRACT|FULL|EPDF|PDF|SUMMARY))?[>|)](LAST)?ACCESSED\d+"
        suffix_regex10 = "[\.|(|,|;]?[A-Z]*\.?SAGEPUB.*?"
        suffix_regex11 = "<[A-Z\/]+>"
        suffix_regex12 = "\.{5}.*?"
        suffix_regex13 = "[\.|,|<|>|&|(|;]"
        suffix_regex14 = "[\.;,]PP.\d+-\d+"
        suffix_regex15 = "[\.|(|,|;]10.\d{4}\/.*?"
        suffix_regex16 = "\[DOI\].*?"
        suffix_regex17 = "\\\\\d{4}[\\\\]?"
        self.suffix_regex_list = [suffix_regex1, suffix_regex2, suffix_regex3, suffix_regex4, suffix_regex5, 
                    suffix_regex6, suffix_regex7, suffix_regex8, suffix_regex9, suffix_regex10, suffix_regex11, 
                    suffix_regex12, suffix_regex13, suffix_regex14, suffix_regex15, suffix_regex16, suffix_regex17]

    def check_dois_validity(self, data:list, field:str, cache_path:str="") -> list:
        checked_dois = list()
        pbar = tqdm(total=len(data))
        doi_logs = dict()
        for row in data:
            rjson = Support().handle_request(url=f"https://doi.org/api/handles/{row[field]}", cache_path=cache_path, error_log_dict=doi_logs)
            if rjson is not None:
                checked_dois.append({"DOI": rjson["handle"], "responseCode": rjson["responseCode"]})
            pbar.update(1)
        pbar.close()
        if len(doi_logs) > 0:
            print("[Support: INFO] Errors have been found. Writing logs to ./doi_logs.json")
            Support().dump_json(doi_logs, "./doi_logs.json")
        return checked_dois
    
    def procedure(self, data:list) -> list:
        successful_output = list()
        statistics = {
            "prefix": 0,
            "suffix": 0,
            "year": 0,
            "other-type": 0
        }
        pbar = tqdm(total=len(data))
        for row in data:
            invalid_doi = row["Invalid_cited_DOI"]
            new_doi, classes_of_errors = self.clean_doi(row["Invalid_cited_DOI"])
            if new_doi != row["Invalid_cited_DOI"]:
                statistics["prefix"] += classes_of_errors["prefix"]
                statistics["suffix"] += classes_of_errors["suffix"]
                statistics["year"] += classes_of_errors["year"]
                statistics["other-type"] += classes_of_errors["other-type"]
                successful_output.append(
                    {"Valid_citing_DOI": row["Valid_citing_DOI"], 
                    "Invalid_cited_DOI": row["Invalid_cited_DOI"],
                    "New_DOI": new_doi, 
                    "prefix_error": classes_of_errors["prefix"],
                    "suffix_error": classes_of_errors["suffix"],
                    "year": classes_of_errors["year"],
                    "other-type": classes_of_errors["other-type"]
                })
            pbar.update(1)
        pbar.close()
        return successful_output, statistics
    
    def clean_doi(self, doi:str) -> str:
        tmp_doi = doi.upper().replace(" ", "")
        prefix_match = re.search(self.prefix_regex, tmp_doi)
        classes_of_errors = {
            "prefix": 0,
            "suffix": 0,
            "year": 0,
            "other-type": 0
        }
        if prefix_match:
            tmp_doi = prefix_match.group(1)
            classes_of_errors["prefix"] += 1
        suffix_match = re.search("(.*?)(?:"+ "|".join(self.suffix_regex_list) + ")$", tmp_doi)
        if suffix_match:
            tmp_doi = suffix_match.group(1)
            classes_of_errors["suffix"] += 1
        year_match = re.search(self.year_regex, tmp_doi)
        if year_match:
            tmp_doi = year_match.group(1)
            classes_of_errors["year"] += 1
        new_doi = re.sub("\\\\", "", tmp_doi)
        new_doi = re.sub("__", "_", tmp_doi)
        new_doi = re.sub("\\.\\.", ".", tmp_doi)
        new_doi = re.sub("<.*?>.*?</.*?>", "", tmp_doi)
        new_doi = re.sub("<.*?/>", "", tmp_doi)
        if new_doi != tmp_doi:
            classes_of_errors["other-type"] += 1
        return new_doi, classes_of_errors



        
    
    

          


        