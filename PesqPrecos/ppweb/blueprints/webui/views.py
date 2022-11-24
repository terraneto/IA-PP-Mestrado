from flask import abort, render_template

from ppweb.models import Product, Uasg
import os

from ppweb.utils import baixa_json_baselicitacoes


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


def view_first_page():
    products = Product.query.all()
    return render_template("index.html", products=products)


def view_second_page():
    products = Product.query.all()
    return render_template("index.html", products=products)


def dir_listing(req_path):
    BASE_DIR = './static/json/'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)


def view_baixa_uasgs():
    baixa_json_baselicitacoes('uasgs')
    return dir_listing('uasgs')
