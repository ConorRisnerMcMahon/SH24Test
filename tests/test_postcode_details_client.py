from app.postcode_details_client import PostcodeDetailsClient, POSTCODES_IO_URL
from hamcrest import assert_that, equal_to, is_
from unittest.mock import patch
import pytest
import requests


@pytest.fixture
def valid_postcode_with_search_result():
    with patch('app.postcode_details_client.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "status": 200,
            "result": {
                "postcode": "SE5 0NF",
                "lsoa": "Southwark 017A"
            }
        }
        return PostcodeDetailsClient(postcode='SE5 0NF')


@pytest.mark.webtest
def test_valid_postcode_with_search_result_fixture_integration():
    resp = requests.get(f'{POSTCODES_IO_URL}/SE5 0NF')
    resp_json = resp.json()
    assert_that(resp_json['status'], equal_to(200))
    assert_that(resp_json['result']['postcode'], equal_to('SE5 0NF'))
    assert_that(isinstance(resp_json['result']['lsoa'], str), is_(True))


@pytest.fixture
def valid_postcode_no_search_result():
    with patch('app.postcode_details_client.requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.json.return_value = {
            "status": 404,
            "error": "Postcode not found"
        }
        return PostcodeDetailsClient(postcode='SH24 1AA')


@pytest.mark.webtest
def test_valid_postcode_no_search_result_fixture_integration():
    resp = requests.get(f'{POSTCODES_IO_URL}/SH24 1AA')
    resp_json = resp.json()
    assert_that(resp_json['status'], equal_to(404))
    assert_that(resp_json['error'], equal_to('Postcode not found'))


@pytest.fixture
def invalid_postcode():
    with patch('app.postcode_details_client.requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.json.return_value = {
            "status": 404,
            "error": "Invalid postcode"
        }
        return PostcodeDetailsClient(postcode='SE13BlahBlah')


@pytest.mark.webtest
def test_invalid_postcode_fixture_integration():
    resp = requests.get(f'{POSTCODES_IO_URL}/SE13BlahBlah')
    resp_json = resp.json()
    assert_that(resp_json['status'], equal_to(404))
    assert_that(resp_json['error'], equal_to('Invalid postcode'))


@pytest.fixture
def failed_search():
    with patch('app.postcode_details_client.requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.json.return_value = {
            "status": 500,
            "error": "Some other error"
        }
        return PostcodeDetailsClient(postcode='SE5 0NF')


def test_can_get_LSOA_for_postcode(valid_postcode_with_search_result):
    assert_that(valid_postcode_with_search_result.lsoa, equal_to('Southwark 017A'))


def test_can_tell_if_search_was_successful(
    valid_postcode_with_search_result,
    valid_postcode_no_search_result,
    invalid_postcode,
    failed_search
):
    assert_that(valid_postcode_with_search_result.search_successful, is_(True))
    assert_that(valid_postcode_no_search_result.search_successful, is_(True))
    assert_that(invalid_postcode.search_successful, is_(True))
    assert_that(failed_search.search_successful, is_(False))


def test_can_tell_if_search_found_a_result(
    valid_postcode_with_search_result,
    valid_postcode_no_search_result,
    invalid_postcode,
    failed_search
):
    assert_that(valid_postcode_with_search_result.result_found, is_(True))
    assert_that(valid_postcode_no_search_result.result_found, is_(False))
    assert_that(invalid_postcode.result_found, is_(False))
    assert_that(failed_search.result_found, is_(False))


def test_can_tell_if_postcode_is_invalid(
    valid_postcode_with_search_result,
    valid_postcode_no_search_result,
    invalid_postcode,
    failed_search
):
    assert_that(valid_postcode_with_search_result.invalid_postcode, is_(False))
    assert_that(valid_postcode_no_search_result.invalid_postcode, is_(False))
    assert_that(invalid_postcode.invalid_postcode, is_(True))
    assert_that(failed_search.invalid_postcode, is_(False))
