from support import Support
from clean_dois import Clean_DOIs

doi_logs = dict()
# To open input csv 
data = Support.process_csv_input(path="./dataset/invalid_dois.csv")
# It is recommended to perform the following step having at least 64GB of RAM, 
# as over 200 million DOIs need to be stored in a set and kept on RAM throughout the following process
# crossref_dois = Support.process_csv_input(path="./dataset/crossref_dois.csv")
# To instantiate the Clean_DOIs class
clean_dois = Clean_DOIs(logs=doi_logs)
# To check if DOIs are valid. The crossref_dois parameter is optional
checked_dois = clean_dois.check_dois_validity(data=data[:100000])
# To clean DOIs
output = clean_dois.procedure(data=checked_dois)
Support().dump_csv(data=output, path="./output.csv")
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
    Support().dump_json(doi_logs, "./logs/doi_logs.json")





