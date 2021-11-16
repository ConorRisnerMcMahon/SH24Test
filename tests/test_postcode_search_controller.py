from hamcrest.core.assert_that import assert_that
from tests.app_fixtures import *
from unittest.mock import patch
from app.postcode_search_controller import postcode_search
from hamcrest import assert_that, is_in, not_


@pytest.fixture
def servable_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.lsoa = 'Newham 007B'
        mock_search.return_value.is_servable = True
        mock_search.return_value.manually_marked_as_servable = True
        mock_search.return_value.in_servable_local_authority = True
        mock_search.return_value.is_invalid_postcode = False
        yield


@pytest.fixture
def not_servable_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.lsoa = 'Newham 007B'
        mock_search.return_value.is_servable = False
        mock_search.return_value.manually_marked_as_servable = False
        mock_search.return_value.in_servable_local_authority = False
        mock_search.return_value.is_invalid_postcode = False
        yield


@pytest.fixture
def no_result_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.lsoa = None
        mock_search.return_value.is_servable = False
        mock_search.return_value.manually_marked_as_servable = False
        mock_search.return_value.in_servable_local_authority = None
        mock_search.return_value.is_invalid_postcode = False
        yield


@pytest.fixture
def invalid_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.lsoa = None
        mock_search.return_value.is_servable = False
        mock_search.return_value.manually_marked_as_servable = False
        mock_search.return_value.in_servable_local_authority = None
        mock_search.return_value.is_invalid_postcode = True
        yield


@pytest.fixture
def failed_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.search_successful = False
        mock_search.return_value.lsoa = None
        mock_search.return_value.is_servable = None
        mock_search.return_value.manually_marked_as_servable = False
        mock_search.return_value.in_servable_local_authority = None
        mock_search.return_value.is_invalid_postcode = None
        yield


@pytest.fixture
def failed_servable_postcode_search():
    with patch(
        'app.postcode_search_controller.search_for_postcode'
    ) as mock_search:
        mock_search.return_value.postcode = 'E7 0NX'
        mock_search.return_value.lsoa = None
        mock_search.return_value.is_servable = True
        mock_search.return_value.manually_marked_as_servable = True
        mock_search.return_value.in_servable_local_authority = None
        mock_search.return_value.is_invalid_postcode = None
        yield


def test_failed_search_returns_500(failed_postcode_search, client):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'An unexpected error has occurred', is_in(resp.data))


def test_failed_search_returns_result_if_postcode_known_servable(
    failed_servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="is_servable"', is_in(resp.data))


def test_servable_search_returns_result(
    servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="is_servable"', is_in(resp.data))
    assert_that(b'test-id="is_not_servable"', not_(is_in(resp.data)))


def test_servable_search_returns_result(
    servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="is_servable"', is_in(resp.data))
    assert_that(b'test-id="is_not_servable"', not_(is_in(resp.data)))


def test_tells_user_if_lsoa_is_servable(
    servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="lsoa_servable"', is_in(resp.data))
    assert_that(b'test-id="lsoa_not_servable"', not_(is_in(resp.data)))


def test_tells_user_if_lsoa_is_not_servable(
    not_servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="lsoa_servable"', not_(is_in(resp.data)))
    assert_that(b'test-id="lsoa_not_servable"', is_in(resp.data))


def test_tells_user_if_postcode_marked_as_servable_manually(
    servable_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="postcode_servable"', is_in(resp.data))


def test_tells_user_if_postcode_is_invalid(
    invalid_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="invalid_postcode"', is_in(resp.data))


def test_tells_user_if_no_lsoa_found(
    no_result_postcode_search, client
):
    resp = client.post('/search', data={'postcode': 'E70NX'})
    assert_that(b'test-id="no_lsoa"', is_in(resp.data))
