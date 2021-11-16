from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    @app.route('/')
    @app.route('/index')
    def index():
        return "Todo...."

    return app