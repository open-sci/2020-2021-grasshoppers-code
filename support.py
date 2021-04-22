import requests, requests_cache, json, csv
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Support(object):
    @staticmethod
    def process_csv_input(path:str) -> list:
        print(f"[Support:INFO Proccessing csv at path ${path}]")
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    
    @staticmethod
    def dump_csv(data:list, path:str):
        print(f"[Support:INFO Writing csv at path ${path}]")
        with open(path, 'w', newline='', encoding='utf8')  as output_file:
            keys = data[0].keys()
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def dump_json(json_data:dict, path:str):
        with open(path, 'w') as outfile:
            print(f"[Support: INFO] Writing json to path ${path}")
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
    
    @staticmethod
    def handle_request(url:str, cache_path:str="", error_log_dict:dict=dict()):
        if cache_path != "":
            requests_cache.install_cache(cache_path)
        try:
            data = self._requests_retry_session().get(url, timeout=60)
            if data.status_code == 200:
                return data.json()
            else:
                error_log_dict[url] = data.status_code
        except Exception as e:
            error_log_dict[url] = str(e)
