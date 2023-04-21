from flask import abort, jsonify
from flask_restful import Resource

from ppweb.models import Material, CNAE, Orgao, Grupo
from ppweb.models import Uasg


class UasgResource(Resource):
    def get(self):
        uasgs = Uasg.query.all() or abort(204)
        return jsonify(
            {"uasgs": [uasg.to_dict() for uasg in uasgs]}
        )


class MaterialResource(Resource):
    def get(self):
        materiais = Material.query.all() or abort(204)
        return jsonify(
            {"materiais": [material.to_dict() for material in materiais]}
        )


class CNAEResource(Resource):
    def get(self):
        cnaes = CNAE.query.all() or abort(204)
        return jsonify(
            {"cnaes": [cnae.to_dict() for cnae in cnaes]}
        )


class OrgaoResource(Resource):
    def get(self):
        orgaos = Orgao.query.all() or abort(204)
        return jsonify(
            {"orgaos": [orgao.to_dict() for orgao in orgaos]}
        )


class GrupoResource(Resource):
    def get(self):
        grupos = Grupo.query.all() or abort(204)
        return jsonify(
            {"grupos": [grupo.to_dict() for grupo in grupos]}
        )


class UasgItemResource(Resource):
    def get(self, id):
        uasg = Uasg.query.filter_by(id=id).first() or abort(404)
        return jsonify(uasg.to_dict())


class MaterialItemResource(Resource):
    def get(self, codigo):
        material = Material.query.filter_by(codigo=codigo).first() or abort(404)
        return jsonify(material.to_dict())
