import requests
from typing import Optional

POSTCODES_IO_URL = 'http://postcodes.io/postcodes'


def get_LSOA(postcode: str) -> Optional[str]:
    resp = requests.get(f'{POSTCODES_IO_URL}/{postcode}')
    resp_json = resp.json()
    if not resp.ok:
        if 'error' in resp_json and resp_json['error'] == 'Postcode not found':
            return None
        else:
            raise ValueError()
    return resp_json['result']['lsoa']
