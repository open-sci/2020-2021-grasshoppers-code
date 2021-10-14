from typing import List, Dict, Set
import csv, json

output = list()

def process_csv_input(path:str) -> list:
    print(f"[Support:INFO Proccessing csv at path {path}]")
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def dump_json(json_data:dict, path:str) -> None:
    with open(path, 'w') as outfile:
        print(f"[Support: INFO] Writing json to path {path}")
        json.dump(json_data, outfile, sort_keys=True, indent=4)

def get_number_of_citations_per_field(data:List[Dict], fields:set) -> int:
    output:Dict[str, set] = dict()
    for field in fields:
        output[field] = set()
    for row in data:
        for field in fields:
            to_be_added = False
            try:
                if int(row[field]) == 1:
                    to_be_added = True
            except ValueError:
                if row[field]:
                    to_be_added = True
            if to_be_added:
                if field == "Valid_citing_DOI":
                    output[field].add(row["Valid_citing_DOI"] + row["Invalid_cited_DOI"])
                else:
                    output[field].add(row["Valid_citing_DOI"] + row["Valid_DOI"])
    return {k:len(v) for k,v in output.items()}


output:List[Dict] = process_csv_input(path="./output/output.csv")
xu:List[Dict] = process_csv_input(path="./output/xu_2019_results.csv")

citations = set()
for row in output:
    citations.add(row["Valid_citing_DOI"] + row["Invalid_cited_DOI"])
print(len(citations))

output = get_number_of_citations_per_field(output, {"Valid_citing_DOI", "Valid_DOI", "Already_valid", "Prefix_error", "Suffix_error", "Other-type_error"})
xu = get_number_of_citations_per_field(xu, {"Valid_citing_DOI", "Valid_DOI", "Prefix_error", "Suffix_error", "Other-type_error"})

output_to_viz = [
    {
        "measure": "DOIs",
        "parent": "",
        "values": [
            {
                "author": "New procedure",
                "value": output["Valid_citing_DOI"]
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": xu["Valid_citing_DOI"]
            }
        ]
    },
    {
        "measure": "Valid_DOI",
        "parent": "DOIs",
        "values": [
            {
                "author": "New procedure",
                "value": output["Valid_DOI"] - output["Already_valid"]
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": xu["Valid_DOI"]
            }
        ]
    },
    {
        "measure": "Prefix_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": output["Prefix_error"]
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": xu["Prefix_error"]
            }
        ]
    },
    {
        "measure": "Suffix_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": output["Suffix_error"]
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": xu["Suffix_error"]
            }
        ]
    },
    {
        "measure": "Other-type_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": output["Other-type_error"]
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": xu["Other-type_error"]
            }
        ]
    }
]

output_to_viz.sort(key = lambda i: i["values"][0]["value"], reverse=True)
dump_json(json_data=output_to_viz, path="./docs/data_to_viz.json")



