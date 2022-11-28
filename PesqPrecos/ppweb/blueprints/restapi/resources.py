from flask import abort, jsonify
from flask_restful import Resource

from ppweb.models import Product
from ppweb.models import Uasg


class ProductResource(Resource):
    def get(self):
        products = Product.query.all() or abort(204)
        return jsonify(
            {"products": [product.to_dict() for product in products]}
        )


class UasgResource(Resource):
    def get(self):
        uasgs = Uasg.query.all() or abort(204)
        return jsonify(
            {"uasgs": [uasg.to_dict() for uasg in uasgs]}
        )


class ProductItemResource(Resource):
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(404)
        return jsonify(product.to_dict())


class UasgItemResource(Resource):
    def get(self, id):
        uasg = Uasg.query.filter_by(id=id).first() or abort(404)
        return jsonify(uasg.to_dict())
