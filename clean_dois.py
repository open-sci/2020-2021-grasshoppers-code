import re
from tqdm import tqdm
from support import Support

class Clean_DOIs(object):
    def __init__(self, cache_path:str="", logs:dict={}):
        self.cache_path = cache_path
        self.logs = logs
        self.prefix_regex = "(.*?)(?:\.)?(?:HTTP:\/\/DX\.D[0|O]I\.[0|O]RG\/|HTTPS:\/\/D[0|O]I\.[0|O]RG\/)(.*)"
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
        suffix_year_regex = "\(\d{4}\)?"
        self.suffix_regex_list = [suffix_regex1, suffix_regex2, suffix_regex3, suffix_regex4, suffix_regex5, 
                    suffix_regex6, suffix_regex7, suffix_regex8, suffix_regex9, suffix_regex10, suffix_regex11, 
                    suffix_regex12, suffix_regex13, suffix_regex14, suffix_regex15, suffix_regex16, suffix_year_regex]

    def check_dois_validity(self, data:list) -> list:
        checked_dois = list()
        pbar = tqdm(total=len(data))
        for row in data:
            invalid_dictionary = {
                "Valid_citing_DOI": row["Valid_citing_DOI"],
                "Invalid_cited_DOI": row["Invalid_cited_DOI"], 
                "Valid_DOI": "",
                "Already_valid": 0
            }
            handle = Support().handle_request(url=f"https://doi.org/api/handles/{row['Invalid_cited_DOI']}", cache_path=self.cache_path, error_log_dict=self.logs)
            if handle is not None:
                if handle["responseCode"] == 1:
                    checked_dois.append(
                        {"Valid_citing_DOI": row["Valid_citing_DOI"],
                        "Invalid_cited_DOI": row["Invalid_cited_DOI"], 
                        "Valid_DOI": row['Invalid_cited_DOI'],
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
            invalid_doi = row["Invalid_cited_DOI"]
            new_doi, classes_of_errors = self.clean_doi(row["Invalid_cited_DOI"])
            valid_dictionary = {
                "Valid_citing_DOI": row["Valid_citing_DOI"], 
                "Invalid_cited_DOI": row["Invalid_cited_DOI"],
                "Valid_DOI": new_doi, 
                "Already_valid": row["Already_valid"],
                "Prefix_error": classes_of_errors["prefix"],
                "Suffix_error": classes_of_errors["suffix"],
                "Other-type_error": classes_of_errors["other-type"]
            }
            invalid_dictionary = {
                "Valid_citing_DOI": row["Valid_citing_DOI"], 
                "Invalid_cited_DOI": row["Invalid_cited_DOI"],
                "Valid_DOI": "", 
                "Already_valid": row["Already_valid"],
                "Prefix_error": classes_of_errors["prefix"],
                "Suffix_error": classes_of_errors["suffix"],
                "Other-type_error": classes_of_errors["other-type"]
            }
            if new_doi != row["Invalid_cited_DOI"]:
                handle = Support().handle_request(url=f"https://doi.org/api/handles/{new_doi}", cache_path=self.cache_path, error_log_dict=self.logs)
                if handle is not None:
                    output.append(valid_dictionary)
                else:
                    output.append(invalid_dictionary)
            else:
                output.append(invalid_dictionary)                                    
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
        suffix_match = re.search("(.*?)(?:"+ "|".join(self.suffix_regex_list) + ")$", tmp_doi)
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



        
    
    

          


        