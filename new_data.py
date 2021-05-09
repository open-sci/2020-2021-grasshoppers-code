from support import Support
from clean_dois import Clean_DOIs

doi_logs = dict()
clean_dois = Clean_DOIs(request_cache="./cache/doi_cache", logs=doi_logs)
checked_dois = Support.process_csv_input(path="./output.csv")
output = clean_dois.procedure(data=checked_dois, cache_path="./cache/output.csv")
Support().dump_csv(data=output, path="./output_new.csv")
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./logs/doi_logs.json")
    Support().dump_json(doi_logs, "./doi_logs.json")





