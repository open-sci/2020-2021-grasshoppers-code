import re
from support import Support

def clean_prefixes(data:list) -> list:
    cleaned_prefixes_dois = list()
    prefixes_regex = "(.*?)(?:\.)?(?:http:\/\/dx\.d[0|o]i\.[0|o]rg\/|https:\/\/doi\.org\/)(.*)"
    for row in data:
        invalid_doi = row["Invalid_cited_DOI"]
        match = re.search(prefixes_regex, invalid_doi, re.IGNORECASE)
        if match:
            new_doi = match.group(1) if match.group(1) > match.group(2) else match.group(2)
            cleaned_prefix_doi = {"Invalid_cited_DOI": row["Invalid_cited_DOI"], "Cleaned_prefix_DOI": new_doi}
            cleaned_prefixes_dois.append(cleaned_prefix_doi)
    return cleaned_prefixes_dois

data = Support().process_csv_input("./dataset/invalid_dois.csv")
clean_prefixes = clean_prefixes(data)
Support().dump_csv(clean_prefixes, './test/clean_prefixes.csv')




