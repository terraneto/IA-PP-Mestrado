from flask import abort, render_template, send_file

from ppweb.models import Product, Uasg, Orgao, Material, Classe, Grupo
import os

from ppweb.utils import baixa_json_baselicitacoes, carrega_json, baixa_json_basemateriais, baixa_json


def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


def uasg():
    uasgs = Uasg.query.all()
    return render_template("uasgs.html", uasgs=uasgs)


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)


def view_home():
    product = Product.query.filter_by(id=1).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)


def dir_listing(req_path):
    BASE_DIR = './static/json/'
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    files = os.listdir(abs_path)
    return render_template('files.html', files=files, vpath=abs_path)


def view_baixa_uasgs():
    baixa_json_baselicitacoes('uasgs', None)
    return dir_listing('uasgs')


def view_baixa_orgaos():
    baixa_json_baselicitacoes('orgaos', 'ativo=True')
    return dir_listing('orgaos')


def view_baixa_tipo_materiais(vtipo):
    print('view baixa tipo de materiais. Tipo=' + vtipo)
    baixa_json_basemateriais(vtipo, None)
    return dir_listing(vtipo)


def view_baixa_json(vmodulo, vtipo):
    print('view baixa tipo de ' + vmodulo + '. Tipo=' + vtipo)
    baixa_json(vmodulo, vtipo, None)
    return dir_listing(vtipo)


def view_carrega_json_uasg():
    carrega_json('uasgs')
    uasgs = Uasg.query.all()
    return render_template("uasgs.html", uasgs=uasgs)


def view_carrega_json_orgao():
    carrega_json('Orgaos')
    orgaos = Orgao.query.all()
    return render_template("orgaos.html", orgaos=orgaos)


def view_carrega_json_materiais():
    carrega_json('materiais')
    materiais = Material.query.all()
    return render_template("material.html", materiais=materiais)
