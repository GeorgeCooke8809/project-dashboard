from flask import Flask
from frontend.routes.api import api
from frontend.routes.pages import pages

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(pages)

    return app