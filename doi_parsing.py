import csv, re

def process_csv_input(path:str) -> list:
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def clean_prefixes(data:list) -> list:
    cleaned_prefixes_dois = list()
    # Wrong regex from https://doi.org/10.1007/s11192-019-03162-4
    # prefixes_regex = "^(?:D[0|O]I\/?HTTP:\/\/DX.D[0|O]I.[0|O]RG\/[0|O]RG\/[:|\/]\\\\d+\\\\.HTTP:\/\/DX.D[0|O]I.[0|O]RG\/?)+(.*)"
    
    # Working regex (in development)
    prefixes_regex = "(?:http:\/\/dx.d[0|o]i.[0|o]rg\/)+(.*)"
    for row in data:
        invalid_doi = row["Invalid_cited_DOI"]
        match = re.search(prefixes_regex, invalid_doi, re.IGNORECASE)
        if match:
            new_doi = match.group(1)
            cleaned_prefix_doi = {"Invalid_cited_DOI": row["Invalid_cited_DOI"], "Cleaned_prefix_DOI": new_doi}
            cleaned_prefixes_dois.append(cleaned_prefix_doi)
    return cleaned_prefixes_dois

def dump_csv(data:list, path:str):
    with open(path, 'w', newline='', encoding='utf-8')  as output_file:
        keys = data[0].keys()
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# data = process_csv_input("./dataset/invalid_dois.csv")
# clean_prefixes = clean_prefixes(data)
# dump_csv(clean_prefixes, './test/clean_prefixes.csv')




