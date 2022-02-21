import random
import re
from csv import DictReader, DictWriter
from clean_dois import Clean_DOIs
from math import ceil
from typing import List, Set, Dict


DATA = './output/output.csv'
# The citations manually checked in the preprint (https://arxiv.org/abs/2111.11263)
PREFERABLE_CITATIONS = './output/100_random_cleaned_dois.csv'
OUTPUT_PATH = './output/10_random_citations_per_rule.csv'


def get_random_results(data:List[dict], number:int=100, preferable_citations:Set[tuple]=None, mandatory_citations:set=None, wanted_patterns:Dict[str, List]=None) -> List[dict]:
    '''
    This function selects a number of random citations within a list. 
    If you specify patterns, the citations will be chosen so that each pattern appears the same number of times within the desired total of citations. 
    The desired total will not be reached if some patterns do not appear in sufficient quantity. 
    You can specify a set of mandatory citations and a set of preferable citations. 
    The former will always be present in the final result, the latter according to the patterns specified and how they are represented within the population.

    :params data: a list of dictionaries representing the content of a CSV file
    :type data: List[dict]
    :params number: the number of random items you want to return
    :type number: int
    :params preferable_citations: a set of citations, where a tuple of two DOIs represents each citation. These citations will be included in the final result only if the patterns specified are sufficiently represented within the population
    :type preferable_citations: Set[tuple]
    :params mandatory_citations: a set of citations, where a tuple of two DOIs represents each citation. These citations will be mandatorily included in the final result
    :type mandatory_citations: Set[tuple]
    :params wanted_patterns: a pattern dictionary, where the keys are the pattern types, while the values consist of patterns' lists of that type. Allowed types are 'Prefix_error', 'Suffix_error' and 'Other-type_error'
    :type wanted_patterns: Dict[str, List]
    :returns: List[dict] -- This function returns a list of dictionaries, that is, a number of random elements from the input list. The result is partially random if the preferred_citations or mandatory_citations parameters were specified
    '''
    output = list()
    included_citations = set()
    if all(arg is None for arg in [preferable_citations, mandatory_citations, wanted_patterns]):
        output = random.sample(
            [i for i in data if len(i['Valid_DOI']) > 0 and int(i['Already_valid']) == 0], 
            number
        )
    if (preferable_citations or mandatory_citations) and not wanted_patterns:
        output.extend(__include_wanted_citations(data, number, included_citations, preferable_citations, mandatory_citations))
    if wanted_patterns:
        number_of_patters = sum(len(patterns) for _, patterns in wanted_patterns.items())
        number_of_matches = ceil(number / number_of_patters)
        for pattern_type, patterns in wanted_patterns.items():
            for pattern in patterns:
                rows_by_pattern = __include_wanted_citations(data, number_of_matches, included_citations, preferable_citations, mandatory_citations, (pattern_type, pattern))
                output.extend(rows_by_pattern)
    return output

def __include_wanted_citations(data:list, number:int, included_citations:Set[tuple], preferable_citations:Set[tuple], mandatory_citations:set=set(), pattern:tuple=None) -> list:
    output = list()
    if mandatory_citations:
        relevant_rows = [row for row in data if (row['Valid_citing_DOI'], row['Invalid_cited_DOI']) in mandatory_citations]
        processed_data, number = __process_wanted_citations(relevant_rows, preferable_citations, number, pattern)
        output.extend(processed_data)
    if preferable_citations:
        processed_data, number = __process_wanted_citations(data, preferable_citations.difference(mandatory_citations), number, pattern)
        output.extend(processed_data)
    included_citations.update({(row['Valid_citing_DOI'], row['Invalid_cited_DOI']) for row in output})
    if number > 0:
        population = list()
        for row in data:
            cur_citation = (row['Valid_citing_DOI'], row['Invalid_cited_DOI'])
            new_citation = cur_citation not in included_citations
            matches_pattern = re.search(pattern[1], row['Invalid_cited_DOI'].upper()) if pattern else True
            error_type = next((error_type for error_type in {'Prefix_error', 'Suffix_error', 'Other-type_error'} if row[error_type] == '1'), None)
            matches_error_type = pattern[0] == error_type if pattern else True
            if row['Valid_DOI'] and row['Already_valid'] == '0' and new_citation and matches_pattern and matches_error_type:
                new_row = {k:v for k,v in row.items()}
                if pattern:
                    new_row['Pattern'] = pattern[1]
                population.append(new_row)
                included_citations.add(cur_citation)
        if len(population) > number:
            output.extend(random.sample(population, number))
        else:
            output.extend(population)
    return output

def __process_wanted_citations(data:list, preferable_citations:set, number:int, pattern:tuple=None) -> list:
    output = list()
    for row in data:
        new_row = {k:v for k,v in row.items()}
        citation = (row['Valid_citing_DOI'], row['Invalid_cited_DOI'])
        relevant_citation = citation in preferable_citations
        if relevant_citation:
            error_type = next(error_type for error_type in {'Prefix_error', 'Suffix_error', 'Other-type_error'} if row[error_type] == '1')
            matches_pattern = re.search(pattern[1], row['Invalid_cited_DOI'].upper()) and pattern[0] == error_type if pattern else True
            if relevant_citation and row['Valid_DOI'] and row['Already_valid'] == '0' and number > 0 and matches_pattern:
                if pattern:
                    new_row['Pattern'] = pattern[1]
                output.append(new_row)
                number -= 1
            elif number == 0:
                break
    return output, number

def get_fields_as_tuples_set(data:list, fields:tuple) -> Set[tuple]:
    tuples_set = set()
    for row in data:
        relevant_data = list()
        for field in fields:
            relevant_data.append(row[field])
        tuples_set.add(tuple(relevant_data))
    return tuples_set

def __check_if_really_valid(source_data:List[dict], target_data:List[dict]) -> List[dict]:
    enriched_data = list()
    for row in target_data:
        source_item = next((item for item in source_data if row['Valid_citing_DOI']==item['Valid_citing_DOI'] and row['Invalid_cited_DOI']==item['Invalid_cited_DOI']), None)
        if source_item:
            row['Really_valid'] = source_item['Really_valid']
        else:
            row['Really_valid'] = ''
        enriched_data.append(row)
    return enriched_data


if __name__ == '__main__':
    regex_worker = Clean_DOIs()
    wanted_patterns = dict()
    wanted_patterns['Suffix_error'] = [f'({regex})$' for regex in regex_worker.suffix_regex_lst]
    wanted_patterns['Prefix_error'] = regex_worker.prefix_regex_lst
    wanted_patterns['Other-type_error'] = ['\\\\', '__', '\\.\\.', '<.*?>.*?</.*?>', '<.*?/>']
    with open(PREFERABLE_CITATIONS, 'r', encoding='utf-8') as f:
        wanted_citation_data = list(DictReader(f))
        # That is, the citations manually checked in the preprint (https://arxiv.org/abs/2111.11263)
        preferable_citations = get_fields_as_tuples_set(data=wanted_citation_data, fields=('Valid_citing_DOI', 'Invalid_cited_DOI'))
    # That is, the two problematic citations already analyzed in the preprint (https://arxiv.org/abs/2111.11263)
    mandatory_citations = {('10.17660/actahortic.2020.1288.20', '10.1007/978-3-319-90698-0_26.'), ('10.1101/539833', '10.1007/s10479-011-0841-3.')}
    with open(DATA, 'r', encoding='utf-8') as f:
        data = list(DictReader(f))
        random_results = get_random_results(data=data, number=230, preferable_citations=preferable_citations, mandatory_citations=mandatory_citations, wanted_patterns=wanted_patterns)
        valid_results = __check_if_really_valid(source_data=wanted_citation_data, target_data=random_results)
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf8')  as output_file:
        print(f"[Support:INFO Proccessing csv at path {OUTPUT_PATH}]")
        keys = ['Valid_citing_DOI', 'Invalid_cited_DOI', 'Valid_DOI', 'Already_valid', 'Prefix_error', 'Suffix_error', 'Other-type_error', 'Pattern', 'Really_valid']
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(valid_results)