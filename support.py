import requests, requests_cache, json, csv, os
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm


class Support(object):
    @staticmethod
    def process_csv_input(path:str) -> list:
        print(f"[Support:INFO Proccessing csv at path {path}]")
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    
    @staticmethod
    def dump_csv(data:list, path:str):
        print(f"[Support:INFO Writing csv at path {path}]")
        with open(path, 'w', newline='', encoding='utf8')  as output_file:
            keys = data[0].keys()
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def dump_json(json_data:dict, path:str):
        with open(path, 'w') as outfile:
            print(f"[Support: INFO] Writing json to path {path}")
            json.dump(json_data, outfile, sort_keys=True, indent=4)

    def _requests_retry_session(
        self,
        tries=1,
        status_forcelist=(500, 502, 504, 520, 521),
        session=None
    ) -> Session:
        session = session or requests.Session()
        retry = Retry(
            total=tries,
            read=tries,
            connect=tries,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def handle_request(self, url:str, cache_path:str="", error_log_dict:dict=dict()):
        if cache_path != "":
            requests_cache.install_cache(cache_path)
        try:
            data = self._requests_retry_session().get(url, timeout=10)
            if data.status_code == 200:
                return data.json()
            else:
                error_log_dict[url] = data.status_code
        except Exception as e:
            error_log_dict[url] = str(e)
    
    @staticmethod
    def get_all_crossref_dois(folder_path:str="./dataset/crossref/"):
        json_files = [pos_json for pos_json in os.listdir(folder_path) if pos_json.endswith('.json')]
        dois = list()
        pbar = tqdm(total=len(json_files))
        for json_file in json_files:
            with open(os.path.join(folder_path, json_file)) as json_file:
                json_text = json.load(json_file)
                for item in json_text["items"]:
                    doi = item["DOI"]
                    dois.append({"crossref_doi": doi})
            pbar.update(1)
        pbar.close()
        return dois
    
    # @staticmethod
    # def get_set_from_list_of_dictionaries(list_item:list, fields:set) -> set:
    #     print(f"[Support: INFO] Getting the set from the dictionaries list")
    #     output_set = set()
    #     for field in fields:
    #         output_set.update({item[field] for item in list_item})
    #     return output_set

crossref_dois = Support.get_all_crossref_dois()
Support.dump_csv(data=crossref_dois, path="./dataset/crossref_dois.csv")
