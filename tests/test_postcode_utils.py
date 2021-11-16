from hamcrest.core.core.isequal import equal_to
from app.postcode_utils import normalise_postcode
from hamcrest import assert_that, equal_to


def test_normalise_postcode_strips_whitespace():
    postcode = normalise_postcode(' S E 2 3BQ ')
    assert_that(postcode, equal_to('SE2 3BQ'))


def test_normalise_postcode_capitalises():
    postcode = normalise_postcode('se2 3bq')
    assert_that(postcode, equal_to('SE2 3BQ'))


def test_normalise_postcode_adds_space_three_characters_back():
    postcode = normalise_postcode('SE23BQ')
    assert_that(postcode, equal_to('SE2 3BQ'))
    postcode = normalise_postcode('SE223BQ')
    assert_that(postcode, equal_to('SE22 3BQ'))
