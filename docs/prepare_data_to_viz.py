from typing import List, Dict
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

output:List[Dict] = process_csv_input(path="./output/output.csv")
xu:List[Dict] = process_csv_input(path="./output/xu_2019_results_no_already_valid.csv")

output_to_viz = [
    {
        "measure": "DOIs",
        "parent": "",
        "values": [
            {
                "author": "New procedure",
                "value": len(output)
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": len(output)
            }
        ]
    },
    {
        "measure": "Invalid_DOI",
        "parent": "DOIs",
        "values": [
            {
                "author": "New procedure",
                "value": len(output)
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": len(output)
            }
        ]
    },
    {
        "measure": "Valid_DOI",
        "parent": "DOIs",
        "values": [
            {
                "author": "New procedure",
                "value": 0
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": 0
            }
        ]
    },
    {
        "measure": "Already_valid",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": 0
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": 0
            }
        ]
    },
    {
        "measure": "Prefix_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": 0
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": 0
            }
        ]
    },
    {
        "measure": "Suffix_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": 0
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": 0
            }
        ]
    },
    {
        "measure": "Other-type_error",
        "parent": "Valid_DOI",
        "values": [
            {
                "author": "New procedure",
                "value": 0
            },
            {
                "author": "Procedure by (Xu et al., 2019)",
                "value": 0
            }
        ]
    }
]

for row in output:
    for k,v in row.items():
        if k == "Valid_DOI" and v != "":
            valid_doi_count = next((item for item in output_to_viz if item["measure"] == k))
            invalid_doi_count = next((item for item in output_to_viz if item["measure"] == "Invalid_DOI"))
            valid_doi_count["values"][0]["value"] += 1
            invalid_doi_count["values"][0]["value"] -= 1
        elif k in ["Already_valid", "Prefix_error", "Suffix_error", "Other-type_error"]:
            class_count = next((item for item in output_to_viz if item["measure"] == k))
            class_count["values"][0]["value"] += int(v)

for row in xu:
    for k,v in row.items():
        if k == "Valid_DOI" and v != "":
            valid_doi_count = next((item for item in output_to_viz if item["measure"] == k))
            invalid_doi_count = next((item for item in output_to_viz if item["measure"] == "Invalid_DOI"))
            valid_doi_count["values"][1]["value"] += 1
            invalid_doi_count["values"][1]["value"] -= 1
        elif k in ["Prefix_error", "Suffix_error", "Other-type_error"]:
            class_count = next((item for item in output_to_viz if item["measure"] == k))
            class_count["values"][1]["value"] += int(v)

output_to_viz.sort(key = lambda i: i["values"][0]["value"], reverse=True)
dump_json(json_data=output_to_viz, path="./docs/data_to_viz.json")



