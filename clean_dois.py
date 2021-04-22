import re
from tqdm import tqdm
from support import Support

class Clean_DOIs(object):
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

    def clean_prefixes(self, data:list, field:str) -> list:
        cleaned_prefixes_dois = list()
        prefixes_regex = "(.*?)(?:\.)?(?:http:\/\/dx\.d[0|o]i\.[0|o]rg\/|https:\/\/doi\.org\/)(.*)"
        for row in data:
            invalid_doi = row[field]
            match = re.search(prefixes_regex, invalid_doi, re.IGNORECASE)
            if match:
                new_doi = match.group(1) if match.group(1) > match.group(2) else match.group(2)
                cleaned_prefix_doi = {"Invalid_DOI": row["Invalid_cited_DOI"], "Cleaned_prefix_DOI": new_doi}
                cleaned_prefixes_dois.append(cleaned_prefix_doi)
        return cleaned_prefixes_dois

        