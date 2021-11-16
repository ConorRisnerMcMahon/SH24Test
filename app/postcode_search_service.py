from app.postcode_details_client import PostcodeDetailsClient
from dataclasses import dataclass
from typing import Optional
from flask import current_app
import json


@dataclass
class SearchResult:
    postcode: str
    lsoa: str = None
    search_successful: bool = None
    is_servable: bool = None
    manually_marked_as_servable: bool = None
    in_servable_local_authority: bool = None
    is_invalid_postcode: bool = None


def in_servable_postcode_list(postcode: str) -> bool:
    servable_postcodes_filepath = current_app.config['SERVABLE_POSTCODES']
    with open(servable_postcodes_filepath, 'r') as file:
        allowed_postcodes = json.load(file)
    return postcode in allowed_postcodes


def in_servable_local_authority_list(lsoa: Optional[str]) -> Optional['bool']:
    if lsoa is None:
        return
    servable_local_authorities_filepath = current_app.config['SERVABLE_LOCAL_AUTHORITIES']
    with open(servable_local_authorities_filepath, 'r') as file:
        allowed_local_authorities = json.load(file)
    for local_authority in allowed_local_authorities:
        if lsoa.startswith(local_authority):
            return True
    return False


def search_for_postcode(postcode: str) -> SearchResult:
    postcode_details = PostcodeDetailsClient(postcode=postcode)
    lsoa = postcode_details.lsoa
    manually_marked_as_servable = in_servable_postcode_list(postcode=postcode)
    in_servable_local_authority = in_servable_local_authority_list(lsoa=lsoa)
    is_servable = manually_marked_as_servable or in_servable_local_authority

    return SearchResult(
        postcode=postcode,
        lsoa=lsoa,
        search_successful=postcode_details.search_successful,
        is_servable=is_servable,
        manually_marked_as_servable=manually_marked_as_servable,
        in_servable_local_authority=in_servable_local_authority,
        is_invalid_postcode=postcode_details.invalid_postcode,
    )
