import tempfile
import json
import os
from app.postcode_search_service import in_servable_postcode_list, in_servable_local_authority_list, search_for_postcode
from hamcrest import is_, assert_that, equal_to, instance_of, none
from unittest.mock import patch
from tests.app_fixtures import *


@pytest.fixture
def servable_postcodes_test_file(app):
    handle, filepath = tempfile.mkstemp()
    with os.fdopen(handle, "w") as f:
        json.dump([
            'SE1 1PQ',
            'E7 0NX'
        ], f
        )
    app.config['SERVABLE_POSTCODES'] = filepath
    yield
    os.unlink(filepath)


@pytest.fixture
def servable_local_authorities_test_file(app):
    handle, filepath = tempfile.mkstemp()
    with os.fdopen(handle, "w") as f:
        json.dump([
            'Lewisham',
            'Newham'
        ], f
        )
    app.config['SERVABLE_LOCAL_AUTHORITIES'] = filepath
    yield
    os.unlink(filepath)


def test_can_load_real_servable_postcode_list(app):
    with app.app_context():
        assert_that(
            in_servable_postcode_list(postcode='SE13 6SE'),
            instance_of(bool)
        )


def test_can_load_real_servable_local_authority_list(app):
    with app.app_context():
        assert_that(
            in_servable_local_authority_list(lsoa='Southwark 123'),
            instance_of(bool)
        )


def test_can_check_if_a_postcode_is_servable(app, servable_postcodes_test_file):
    with app.app_context():
        assert_that(
            in_servable_postcode_list(postcode='SE13 6SE'),
            is_(False)
        )
        assert_that(
            in_servable_postcode_list(postcode='E7 0NX'),
            is_(True)
        )


def test_can_check_if_lsoa_is_servable(app, servable_local_authorities_test_file):
    with app.app_context():
        assert_that(
            in_servable_local_authority_list(lsoa='Newham 007B'),
            is_(True)
        )
        assert_that(
            in_servable_local_authority_list(lsoa='Hackney 019A'),
            is_(False)
        )


def test_check_if_lsoa_is_servable_returns_none_when_lsoa_is_none():
    assert_that(in_servable_local_authority_list(lsoa=None), none())


@patch('app.postcode_search_service.PostcodeDetailsClient')
def test_can_create_a_search_result(
    mock_search_client,
    app,
    servable_postcodes_test_file,
    servable_local_authorities_test_file
):
    mock_search_client.return_value.postcode = 'E7 0NX'
    mock_search_client.return_value.lsoa = 'Newham 007B'
    mock_search_client.return_value.search_successful = True
    mock_search_client.return_value.invalid_postcode = False

    with app.app_context():
        search_result = search_for_postcode('E7 0NX')

    assert_that(search_result.postcode, equal_to('E7 0NX'))
    assert_that(search_result.lsoa, equal_to('Newham 007B'))
    assert_that(search_result.is_servable, is_(True))
    assert_that(search_result.manually_marked_as_servable, is_(True))
    assert_that(search_result.in_servable_local_authority, is_(True))
    assert_that(search_result.is_invalid_postcode, is_(False))
