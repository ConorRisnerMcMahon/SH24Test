import requests
from typing import Optional

POSTCODES_IO_URL = 'http://postcodes.io/postcodes'


class PostcodeDetailsClient:

    def __init__(self, postcode: str) -> None:
        self.postcode = postcode
        resp = requests.get(f'{POSTCODES_IO_URL}/{self.postcode}')
        self.search_result = resp.json()

    @property
    def status(self) -> int:
        return self.search_result['status']

    @property
    def search_successful(self) -> bool:
        return self.result_found or self.result_not_found or self.invalid_postcode

    @property
    def result_found(self) -> bool:
        return self.status == 200

    @property
    def result_not_found(self) -> bool:
        return self.status == 404 and self.search_result['error'] == 'Postcode not found'

    @property
    def invalid_postcode(self) -> bool:
        return self.status == 404 and self.search_result['error'] == 'Invalid postcode'

    @property
    def lsoa(self) -> Optional['str']:
        if self.result_found:
            return self.search_result['result']['lsoa']
