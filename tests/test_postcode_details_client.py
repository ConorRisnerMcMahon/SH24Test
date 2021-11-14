from app.postcode_details_client import PostcodeDetailsClient
from hamcrest import assert_that, equal_to, is_
from unittest.mock import patch
import pytest


@patch('app.postcode_details_client.requests.get')
def test_can_get_LSOA_for_postcode(mock_get):
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200,
        "result": {
            "postcode": "SE5 0NF",
            "lsoa": "Southwark 017A"
        }
    }
    assert_that(postcode_details_client.lsoa, equal_to('Southwark 017A'))


@pytest.mark.webtest
def test_can_get_LSOA_for_postcode_webtest():
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    assert_that(postcode_details_client.lsoa, equal_to('Southwark 017A'))


@patch('app.postcode_details_client.requests.get')
def test_repeated_access_to_search_result_only_makes_one_request(mock_get):
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200,
        "result": {
            "postcode": "SE5 0NF",
            "lsoa": "Southwark 017A"
        }
    }
    mock_get.assert_not_called()
    postcode_details_client.lsoa
    mock_get.assert_called_once()
    postcode_details_client.lsoa
    mock_get.assert_called_once()


@patch('app.postcode_details_client.requests.get')
def test_can_tell_if_a_search_result_was_returned(mock_get):
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 NF')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 404,
        "error": "Invalid postcode"
    }
    assert_that(postcode_details_client.result_found, is_(False))
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200,
        "result": {
            "postcode": "SE5 0NF",
            "lsoa": "Southwark 017A"
        }
    }
    assert_that(postcode_details_client.result_found, is_(True))


@pytest.mark.webtest
def test_can_tell_if_a_search_result_was_returned_webtest():
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 NF')
    assert_that(postcode_details_client.result_found, is_(False))
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    assert_that(postcode_details_client.result_found, is_(True))


@patch('app.postcode_details_client.requests.get')
def test_can_tell_if_a_postcode_is_invalid(mock_get):
    postcode_details_client = PostcodeDetailsClient(postcode='SE13BlahBlah')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 404,
        "error": "Invalid postcode"
    }
    assert_that(postcode_details_client.invalid_postcode, is_(True))
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200
    }
    assert_that(postcode_details_client.invalid_postcode, is_(False))
    postcode_details_client = PostcodeDetailsClient(postcode='SH24 1AA')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 200,
        "error": "Postcode not found"
    }
    assert_that(postcode_details_client.invalid_postcode, is_(False))


@pytest.mark.webtest
def test_can_tell_if_a_postcode_is_invalid_webtest():
    postcode_details_client = PostcodeDetailsClient(postcode='SE13BlahBlah')
    assert_that(postcode_details_client.invalid_postcode, is_(True))
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    assert_that(postcode_details_client.invalid_postcode, is_(False))
    postcode_details_client = PostcodeDetailsClient(postcode='SH24 1AA')
    assert_that(postcode_details_client.invalid_postcode, is_(False))


@patch('app.postcode_details_client.requests.get')
def test_search_failed_to_return_result_for_unknown_reason(mock_get):
    postcode_details_client = PostcodeDetailsClient(postcode='SE13BlahBlah')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 404,
        "error": "Invalid postcode"
    }
    assert_that(postcode_details_client.search_successful, is_(True))
    postcode_details_client = PostcodeDetailsClient(postcode='SE5 0NF')
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200
    }
    assert_that(postcode_details_client.search_successful, is_(True))
    postcode_details_client = PostcodeDetailsClient(postcode='SH24 1AA')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 200,
        "error": "Postcode not found"
    }
    assert_that(postcode_details_client.search_successful, is_(True))
    postcode_details_client = PostcodeDetailsClient(postcode='SH24 1AA')
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 500,
        "error": "Some other error"
    }
    assert_that(postcode_details_client.search_successful, is_(False))
