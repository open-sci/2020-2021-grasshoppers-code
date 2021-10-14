from support import Support, get_number_of_citations
from clean_dois import Clean_DOIs


# To open input csv 
data = Support.process_csv_input(path="./dataset/invalid_dois.csv")

# It is recommended to perform the following step having at least 64GB of RAM, 
# as over 200 million DOIs need to be stored in a set and kept on RAM throughout the following process
# crossref_dois = Support.process_csv_input(path="./dataset/crossref_dois.csv")

# To instantiate the Clean_DOIs class
doi_logs = dict()
clean_dois = Clean_DOIs(logs=doi_logs)

# To check if DOIs are valid. The crossref_dois parameter is optional
checked_dois = clean_dois.check_dois_validity(data=data, autosave_path="./cache/checked_dois.csv")

# # To clean DOIs
output = clean_dois.procedure(data=checked_dois, autosave_path="./cache/output.csv")
Support().dump_csv(data=output, path="./output/output.csv")
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
    Support().dump_json(doi_logs, "./logs/doi_logs.json")

# To get the number of matches of each sub-class of factual errors
output = Support.process_csv_input(path="./output/output.csv")
number_of_matches = clean_dois.get_number_of_matches(data=output)
print(number_of_matches)

# To get the number of valid citations after the cleaning procedure
output = Support.process_csv_input(path="./output/output.csv")
xu = Support.process_csv_input(path="./output/xu_2019_results.csv")
data = [output, xu]
number_of_citations = get_number_of_citations(data=data)
print(number_of_citations)



