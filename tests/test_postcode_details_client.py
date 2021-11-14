from app.postcode_details_client import get_LSOA
from hamcrest import assert_that, equal_to
from unittest.mock import patch
import pytest


@patch('app.postcode_details_client.requests.get')
def test_can_get_LSOA_for_postcode(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "status": 200,
        "result": {
            "postcode": "SE5 0NF",
            "lsoa": "Southwark 017A"
        }
    }
    LSOA = get_LSOA('SE5 0NF')
    assert_that(LSOA, equal_to('Southwark 017A'))


@pytest.mark.webtest
def test_can_get_LSOA_for_postcode_webtest():
    LSOA = get_LSOA('SE5 0NF')
    assert_that(LSOA, equal_to('Southwark 017A'))


@patch('app.postcode_details_client.requests.get')
def test_get_LS0A_for_invalid_postcode_raises_error(mock_get):
    mock_get.return_value.ok = False
    mock_get.return_value.json.return_value = {
        "status": 404,
        "error": "Invalid postcode"
    }
    with pytest.raises(ValueError):
        get_LSOA('SE5 NF')


@pytest.mark.webtest
def test_get_LS0A_for_invalid_postcode_raises_error_webtest():
    with pytest.raises(ValueError):
        get_LSOA('SE5 NF')
