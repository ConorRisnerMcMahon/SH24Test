from flask import Flask, redirect, url_for, render_template
from werkzeug.exceptions import InternalServerError


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config.from_object('app.config.Testing')
    else:
        app.config.from_object('app.config.Config')

    @app.route('/')
    @app.route('/index')
    def index():
        return redirect(url_for('search'))

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        from app.postcode_search_controller import postcode_search
        return postcode_search()

    @app.route('/<postcode>')
    def view_postcode(postcode):
        from app.postcode_search_controller import view_postcode_details
        return view_postcode_details(postcode)

    @app.errorhandler(InternalServerError)
    def handle_500(e):
        return render_template('500.html'), 500

    return app
