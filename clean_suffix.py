import csv, re


def process_csv_input(path:str) -> list:
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def clean_suffixes(data: list) -> list:
    cleaned_suffixes_dois = list()
    regex1 = "\/-\/DCSUPPLEMENTAL"
    regex2 = "SUPPINF[0|O](\.)?"
    regex3 = "[\.|(|,|;]?PMID:\d+.*?"
    regex4 = "[\.|(|,|;]?PMCID:PMC\d+.*?"
    regex5 = "[(|\[]EPUBAHEADOFPRINT[)\]]"
    regex6 = "[\.|(|,|;]?ARTICLEPUBLISHEDONLINE.*?\d{4}"
    regex7 = "[\.|(|,|;]*HTTP:\/\/.*?"
    regex8 = "[\.\/](META|ABSTRACT|FULL|EPDF|PDF|SUMMARY)>?"
    regex9 = "([\/\.](META|ABSTRACT|FULL|EPDF|PDF|SUMMARY))?[>|)](LAST)?ACCESSED\d+"
    regex10 = "[\.|(|,|;]?[A-Z]*\.?SAGEPUB.*?"
    regex11 = "<[A-Z\/]+>"
    regex12 = "\.{5}.*?"
    regex13 = "[\.|,|<|>|&|(|;]"
    regex14 = "[\.;,]PP.\d+-\d+"
    regex15 = "[\.|(|,|;]10.\d{4}\/.*?"
    regex16 = "\[DOI\].*?"
    regex17 = "\\\\\d{4}[\\\\]?"

    regex_lst = [regex1, regex2, regex3, regex4, regex5, regex6, \
                 regex7, regex8, regex9, regex10, regex11, regex12, regex13, regex14, regex15]
    for row in data:
        invalid_doi = row["Invalid_cited_DOI"]
        match = re.search("(.*?)(?:"+ "|".join(regex_lst) + ")$", invalid_doi.upper())
        if match:
            new_doi = match.group(1)
            cleaned_suffix_doi = {"Invalid_cited_DOI": row["Invalid_cited_DOI"], "Cleaned_suffix_DOI": new_doi}
            cleaned_suffixes_dois.append(cleaned_suffix_doi)

    return cleaned_suffixes_dois


data = process_csv_input("../invalid_dois.csv")
clean_suffixs = clean_suffixes(data)
print(len(clean_suffixs))
