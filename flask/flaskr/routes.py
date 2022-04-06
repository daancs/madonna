from flask import Blueprint

routes_blueprint = Blueprint('paths', __name__)

@routes_blueprint.route('/')
def hello():
    return 'Hello, World!'
