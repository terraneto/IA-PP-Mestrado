from flask import Blueprint
from flask_restful import Api

from .resources import UasgItemResource, UasgResource, MaterialResource, \
    MaterialItemResource, CNAEResource, OrgaoResource, GrupoResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(UasgResource, "/uasg/")
    api.add_resource(UasgItemResource, "/uasg/<id>")
    api.add_resource(MaterialResource, "/material/")
    api.add_resource(MaterialItemResource, "/material/<codigo>")
    api.add_resource(CNAEResource, "/cnae/")
    api.add_resource(OrgaoResource, "/orgao/")
    api.add_resource(GrupoResource, "/grupo/")
    app.register_blueprint(bp)
