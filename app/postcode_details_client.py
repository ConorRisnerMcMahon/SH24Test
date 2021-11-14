import requests
from typing import Optional

POSTCODES_IO_URL = 'http://postcodes.io/postcodes'


class PostcodeDetailsClient:

    def __init__(self, postcode: str) -> None:
        self.postcode = postcode
        self.response = None

    def search(self):
        resp = requests.get(f'{POSTCODES_IO_URL}/{self.postcode}')
        self.response = resp.json()

    @property
    def search_result(self):
        if self.response is None:
            self.search()
        return self.response

    @property
    def result_found(self) -> bool:
        if self.search_result['status'] == 200:
            return True
        return False

    @property
    def lsoa(self) -> Optional['str']:
        if self.result_found:
            return self.search_result['result']['lsoa']
