from flask import Blueprint
from flask_restful import Api

from pokedex.models.database import db
import pokedex

from .pokemons import Pokemon, Pokemons
from .types import Types

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


def register_api(app):
    @api_bp.before_request
    def before_request():
        db.connect(reuse_if_open=True)
        pass

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()

    @api_bp.errorhandler(pokedex.errors.NotFoundError)
    def if_not_found(error):
        response = {"error": f"{error.resource} {error.resource_id} not found"}
        return response, 404

    api.add_resource(Pokemons, "/pokemons")
    api.add_resource(Pokemon, "/pokemon/<pokemon_name>")
    api.add_resource(Types, "/types")

    app.register_blueprint(api_bp, url_prefix="/api/v1")
