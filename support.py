# ISC License (ISC)
# ==================================
# Copyright 2021 Arcangelo Massari, Cristian Santini, Ricarda Boente, Deniz Tural

# Permission to use, copy, modify, and/or distribute this software for any purpose with or
# without fee is hereby granted, provided that the above copyright notice and this permission
# notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import requests, requests_cache, json, csv, os, ijson
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
            data = self._requests_retry_session().get(url, timeout=5)
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
                parser = ijson.parse(json_file)
                for prefix, event, value in parser:
                    if (prefix, event) == ('items.item.DOI', 'string'):
                        dois.append({"crossref_doi": value})
            pbar.update(1)
        pbar.close()
        return dois
            