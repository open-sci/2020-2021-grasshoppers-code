import csv
from support import Support
from clean_dois import Clean_DOIs

doi_logs = dict()
clean_dois = Clean_DOIs(cache_path="./cache/doi_cache", logs=doi_logs)

# To open input csv 
data = Support.process_csv_input(path="./dataset/invalid_dois.csv")
crossref_dois = Support.process_csv_input(path="./dataset/crossref_dois.csv")
# To transform the csv with the DOIs taken from Crossref into a set, so that accessing it is much more efficient
crossref_dois = {item["crossref_doi"] for item in crossref_dois}
# To check if DOIs are valid
checked_dois = clean_dois.check_dois_validity(data=data, crossref_dois=crossref_dois)
# To clean DOIs
output = clean_dois.procedure(data=checked_dois)
Support().dump_csv(data=output, path="./output.csv")
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
    Support().dump_json(doi_logs, "./logs/doi_logs.json")





