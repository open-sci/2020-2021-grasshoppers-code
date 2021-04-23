import csv
from support import Support
from clean_dois import Clean_DOIs

clean_dois = Clean_DOIs()

# To open input csv 
data = Support().process_csv_input(path="./dataset/invalid_dois.csv")

# To check if DOIs are valid
# checked_dois = clean_dois.check_dois_validity(data=data, field="Invalid_cited_DOI", cache_path="./cache/doi_cache")

# To dump list of dictionaries as csv
# Support().dump_csv(data=checked_dois, path="./test/checked_dois2.csv")

# To clean invalid prefixes 
# clean_prefixes = clean_dois.clean_prefixes(data=data, field="Invalid_cited_DOI")
# checked_dois = clean_dois.check_dois_validity(data=clean_prefixes, field="Cleaned_prefix_DOI", cache_path="./cache/doi_cache")
# Support().dump_csv(data=checked_dois, path="./test/clean_prefixes.csv")

clean_year, statistics = clean_dois.procedure(data=data)
print(statistics)
Support().dump_csv(data=clean_year, path="./test/clean_year.csv")




