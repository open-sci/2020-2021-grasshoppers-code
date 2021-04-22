import csv
from support import Support
from tqdm import tqdm

data = Support().process_csv_input(path="./dataset/invalid_dois.csv")

with open("doi_check.csv", "w", newline='', encoding='utf8') as result:
    csv_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['DOI', 'ResponseCode'])
    pbar = tqdm(total=len(data))
    doi_logs = dict()
    for row in data:
        rjson = Support().handle_request(url=f"https://doi.org/api/handles/{row['Invalid_cited_DOI']}", cache_path="./cache/doi_cache", error_log_dict=doi_logs)
        if rjson is not None:
            csv_writer.writerow([rjson["handle"], str(rjson["responseCode"])])
        pbar.update(1)
    pbar.close()

if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./doi_logs.json")
    Support().dump_json(doi_logs, "./doi_logs.json")

