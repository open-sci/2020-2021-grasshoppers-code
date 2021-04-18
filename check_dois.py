import requests as req
import csv

with open("invalid_dois.csv", encoding='Latin1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    with open("doi_check.csv", "w", newline='', encoding='Latin1') as result:
        csv_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['DOI', 'ResponseCode'])
        for row in csv_reader:
            if row[0] != "Valid_citing_DOI":
                r = req.get("https://doi.org/api/handles/" + row[1])
                rjson = r.json()
                csv_writer.writerow([rjson["handle"], str(rjson["responseCode"])])
                if rjson["responseCode"] != 100:
                    print(rjson["handle"] + ",Code " + str(rjson["responseCode"]))
