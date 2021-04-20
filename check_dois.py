import csv
from support import Support
from tqdm import tqdm

doi_logs = dict()
data = list()
# It is better not to work with an open file, because it can only be read once,
# after which the cursor is exhausted and the file can no longer be read. 
# It is better to save the contents of the file in a variable, 
# so that the other functions written by Cristian, Deniz and me can also operate on it. 
# I would also propose to create a unique function that manages the processing of the initial data. 
with open("./dataset/invalid_dois.csv", encoding='Latin1') as csv_file:
    # I'm curious on why you chose Latin1 instead of utf8
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    data.extend(csv_reader)

with open("doi_check.csv", "w", newline='', encoding='Latin1') as result:
    csv_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['DOI', 'ResponseCode'])
    # This library allows you to view a loading bar and the expected remaining time in the terminal
    pbar = tqdm(total=len(data))
    for row in data:
        # In order not to mess up your code, I have created a Support class that deals with handling 
        # the various exceptions that may occur during a request, so that the execution does not crash and, 
        # in case of errors, it arrives at the end showing some log on what went wrong.
        rjson = Support().handle_request(url=f"https://doi.org/api/handles/{row['Invalid_cited_DOI']}", cache_path="./doi_cache", error_log_dict=doi_logs)
        if rjson is not None:
            csv_writer.writerow([rjson["handle"], str(rjson["responseCode"])])
            if rjson["responseCode"] != 100:
                print(rjson["handle"] + ",Code " + str(rjson["responseCode"]))
        pbar.update(1)
    pbar.close()
# In this way, many hours are still required to complete the function, 
# but at least you know where it is and, unless the PC turns off, it should not crash.
if len(doi_logs) > 0:
    print("[Support: INFO] Errors have been found. Writing logs to ./doi_logs.json")
    Support().dump_json(doi_logs, "./doi_logs.json")

