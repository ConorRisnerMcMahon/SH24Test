from flask import render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from app.postcode_search_service import search_for_postcode
from app.postcode_utils import normalise_postcode


class PostcodeSearchForm(FlaskForm):
    postcode = StringField('Postcode:')
    submit = SubmitField('Search!')


def postcode_search():
    form = PostcodeSearchForm()
    if form.validate_on_submit():
        postcode = form.postcode.data
        postcode = normalise_postcode(postcode)
        return(view_postcode_details(postcode))
    return render_template('postcode_search.html', form=form)


def view_postcode_details(postcode: str):
    search_result = search_for_postcode(postcode=postcode)

    if not search_result.search_successful:
        if not search_result.is_servable:
            abort(500)

    return render_template(
        'postcode_details.html',
        postcode=search_result.postcode,
        lsoa=search_result.lsoa,
        is_servable=search_result.is_servable,
        manually_marked_as_servable=search_result.manually_marked_as_servable,
        in_servable_local_authority=search_result.in_servable_local_authority,
        is_invalid_postcode=search_result.is_invalid_postcode,
    )
