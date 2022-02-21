import unittest
from clean_dois import Clean_DOIs
from csv import DictReader
from evaluation import get_random_results, get_fields_as_tuples_set


DATA = './output/output.csv'
# The citations manually checked in the preprint (https://arxiv.org/abs/2111.11263)
PREFERABLE_CITATIONS = './output/100_random_cleaned_dois.csv'
OUTPUT_PATH = './output/10_random_cleaned_dois_per_rule.csv'


def prepare_data(preferable_citations:str=PREFERABLE_CITATIONS, data:str=DATA):
    regex_worker = Clean_DOIs()
    wanted_patterns = dict()
    wanted_patterns['Suffix_error'] = [f'({regex})$' for regex in regex_worker.suffix_regex_lst]
    wanted_patterns['Prefix_error'] = regex_worker.prefix_regex_lst
    wanted_patterns['Other-type_error'] = ['\\\\', '__', '\\.\\.', '<.*?>.*?</.*?>', '<.*?/>']
    with open(preferable_citations, 'r', encoding='utf-8') as f:
        wanted_citation_data = list(DictReader(f))
        # That is, the citations manually checked in the preprint (https://arxiv.org/abs/2111.11263)
        preferable_citations = get_fields_as_tuples_set(data=wanted_citation_data, fields=('Valid_citing_DOI', 'Invalid_cited_DOI'))
    mandatory_citations = {('10.17660/actahortic.2020.1288.20', '10.1007/978-3-319-90698-0_26.'), ('10.1101/539833', '10.1007/s10479-011-0841-3.')}
    with open(data, 'r', encoding='utf-8') as f:
        data = list(DictReader(f))
    return data, wanted_patterns, mandatory_citations, preferable_citations


class test_evaluation(unittest.TestCase):
    def test_get_random_results_no_duplicates(self):
        # This test verifies that there are not duplicated citations in the output
        data, wanted_patterns, mandatory_citations, preferable_citations = prepare_data(preferable_citations=PREFERABLE_CITATIONS, data=DATA)
        output = get_random_results(data=data, number=230, preferable_citations=preferable_citations, mandatory_citations=mandatory_citations, wanted_patterns=wanted_patterns)
        citations = set()
        duplicated_citations = set()
        for row in output:
            citation = (row['Valid_citing_DOI'], row['Invalid_cited_DOI'])
            if citation in citations:
                duplicated_citations.add(citation)
                print(citation)
            citations.add(citation)
        self.assertEqual(len(duplicated_citations), 0)
    
    def test_get_random_results_output_length(self):
        data, _, mandatory_citations, preferable_citations = prepare_data(preferable_citations=PREFERABLE_CITATIONS, data=DATA)
        output = get_random_results(data=data, number=10, preferable_citations=preferable_citations, mandatory_citations=mandatory_citations)
        self.assertEqual(len(output), 10)
    
    def test_get_random_results_base_operation(self):
        data, _, _, _ = prepare_data(preferable_citations=PREFERABLE_CITATIONS, data=DATA)
        output = get_random_results(data=data, number=10)
        self.assertEqual(len(output), 10)


if __name__ == '__main__':
    unittest.main()