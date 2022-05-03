import os

from flask import Flask
from . import auth
from . import nav
from . import home
from . import db
from . import guiQuery

# from routes import routes_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
   # db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(nav.bp)
    app.register_blueprint(guiQuery.bp)
    app.register_blueprint(home.bp)

    app.add_url_rule('/', endpoint='index')

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # app.register_blueprint(routes)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hej, Clara!'

    return app


