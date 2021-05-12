from clean_dois import *
from support import *
import unittest

class Test_Clean_DOIs(unittest.TestCase):
    def test_clean_doi_prefix(self):
        self.assertEqual(Clean_DOIs().clean_doi("10.1016/j.aca.2006.07.086.http://dx.doi.org/10.1016/j.aca.2006.07.086"), ("10.1016/j.aca.2006.07.086", {"prefix": 1, "suffix": 0, "other-type": 0}))
    def test_clean_doi_suffix(self):
        self.assertEqual(Clean_DOIs().clean_doi("10.1186/1735-2746-10-21,http://www.ijehse.com/content/10/1/21"), ("10.1186/1735-2746-10-21", {"prefix": 0, "suffix": 1, "other-type": 0}))
    def test_clean_doi_other_type(self):
        self.assertEqual(Clean_DOIs().clean_doi("10.1186/1471-2407-13-87<br/>"), ("10.1186/1471-2407-13-87", {"prefix": 0, "suffix": 0, "other-type": 1}))
    def test_procedure(self):
        input_data = [{"Valid_citing_DOI":"10.1177/1550059416645980", "Invalid_cited_DOI":"10.1016/j.biopsych.2005.08.030.", "Valid_DOI": "", "Already_valid": 0}]
        expected_output = [{
            "Valid_citing_DOI": "10.1177/1550059416645980",
            "Invalid_cited_DOI": "10.1016/j.biopsych.2005.08.030.",
            "Valid_DOI": "10.1016/j.biopsych.2005.08.030",
            "Already_valid": 0,
            "Prefix_error": 0,
            "Suffix_error": 1,
            "Other-type_error": 0
        }]
        self.assertEqual(Clean_DOIs().procedure(input_data), expected_output)
    def test_check_dois_validity(self):
        input_data = [{"Valid_citing_DOI":"10.1007/s11771-020-4410-2", "Invalid_cited_DOI":"10.13745/j.esf.2016.02.011"}]
        expected_output = [{
            "Valid_citing_DOI": "10.1007/s11771-020-4410-2",
            "Invalid_cited_DOI": "10.13745/j.esf.2016.02.011",
            "Valid_DOI": "10.13745/j.esf.2016.02.011",
            "Already_valid": 1
        }]
        self.assertEqual(Clean_DOIs().check_dois_validity(data=input_data), expected_output)
    def test_get_number_of_matches(self):
        input_data = [{"Valid_citing_DOI":"10.1007/s11771-020-4410-2", "Invalid_cited_DOI":"10.13745/j.esf.2016.02.011"}]
        expected_output = {
            'other-type': {
                '\\\\': 0, 
                '__': 0, 
                '\\.\\.': 0, 
                '<.*?>.*?</.*?>': 0, 
                '<.*?/>': 0}, 
            'prefix': {
                'HTTP:\\/\\/DX\\.D[0|O]I\\.[0|O]RG\\/': 0, 
                'HTTPS:\\/\\/D[0|O]I\\.[0|O]RG\\/': 0}, 
            'suffix': {
                '\\/-\\/DCSUPPLEMENTAL': 0, 
                'SUPPINF[0|O](\\.)?': 0, 
                '[\\.|\\(|,|;]?PMID:\\d+.*?': 0, 
                '[\\.|\\(|,|;]?PMCID:PMC\\d+.*?': 0, 
                '[\\(|\\[]EPUBAHEADOFPRINT[\\)\\]]': 0, 
                '[\\.|\\(|,|;]?ARTICLEPUBLISHEDONLINE.*?\\d{4}': 0, 
                '[\\.|\\(|,|;]*HTTP:\\/\\/.*?': 0, 
                '\\/(META|ABSTRACT|FULL|EPDF|PDF|SUMMARY)([>|\\)](LAST)?ACCESSED\\d+)?': 0, 
                '[>|\\)](LAST)?ACCESSED\\d+': 0, 
                '[\\.|\\(|,|;]?[A-Z]*\\.?SAGEPUB.*?': 0, 
                '\\.{5}.*?': 0, 
                '[\\.|,|<|&|\\(|;]+': 1, 
                '\\[DOI\\].*?': 0, 
                '\\(\\d{4}\\)?': 0, 
                '\\?.*?=.*?': 0, 
                '#.*?': 0
            }
        }
        self.assertEqual(Clean_DOIs().get_number_of_matches(data=input_data), expected_output)


if __name__ == '__main__':
    unittest.main()
