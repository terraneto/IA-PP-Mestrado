from flask import abort, render_template, send_file, request, jsonify

from ppweb.models import Product, Uasg, Orgao, Material, Classe, Grupo, PDM

import os

from ppweb.utils import carrega_json, baixa_json, baixa_json_contratos_mensal, baixa_json_diario, baixa_material_por_id


def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


def get_dropdown_values():
    modulos = {
        'fornecedores': ['ambitos_ocorrencia', 'cnaes', 'fornecedores', 'linhas_fornecimento', 'municipios',
                         'naturezas_juridicas', 'ocorrencias_fornecedores', 'portes_empresa', 'prazos_ocorrencia',
                         'ramos_negocio', 'tipos_ocorrencia'],
        'materiais': ['classes', 'grupos', 'pdms', 'materiais']
    }
    return modulos


def update_dropdown():
    print('entrei no update dropdown')
    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown

    updated_values = get_dropdown_values()[selected_class]
    print(updated_values)
    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    jsonify(random_text="You selected the car brand: {} and the model: {}.".format(selected_class, selected_entry))
    baixa_json(selected_class, selected_entry, None)
    return dir_listing(selected_entry)


def view_seltipo():
    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    return render_template('seltipo.html',
                           all_classes=default_classes,
                           all_entries=default_values)


"""    return render_template(
        "seltipo.html",
        modulos=[{'label': 'Contratos desde 2021', 'modulo': 'comprasContratos'},
                 {'label': 'Fornecedores', 'modulo': 'fornecedores'},
                 {'label': 'Licitações', 'modulo': 'licitacoes'},
                 {'label': 'Materiais', 'modulo': 'materiais'}]
    )
"""


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


def view_baixa_json(vmodulo, vtipo):
    print('view baixa tipo de ' + vmodulo + '. Tipo=' + vtipo)
    baixa_json(vmodulo, vtipo, None)
    return dir_listing(vtipo)


def view_baixa_json_contratos_mensal(vmodulo, vtipo, vano):
    print('view baixa tipo de ' + vmodulo + '. Tipo=' + vtipo + ' Ano=' + str(vano))
    baixa_json_contratos_mensal(vmodulo, vtipo, vano)
    return dir_listing(vtipo)


def view_baixa_json_diario(vmodulo, vtipo, vano):
    print('view baixa tipo de ' + vmodulo + '. Tipo=' + vtipo + ' Ano=' + str(vano))
    baixa_json_diario(vmodulo, vtipo, vano)
    return dir_listing(vtipo)


def view_baixa_material_por_id():
    print('view baixa material por id')
    baixa_material_por_id()
    return dir_listing('material')


def view_carrega_json_uasg():
    carrega_json('uasgs')
    uasgs = Uasg.query.all()
    return render_template("uasgs.html", uasgs=uasgs)


def view_carrega_json_orgao():
    carrega_json('Orgaos')
    orgaos = Orgao.query.all()
    return render_template("orgaos.html", orgaos=orgaos)


def view_carrega_json_classes():
    carrega_json('classes')
    classes = Classe.query.all()
    return render_template("classes.html", classes=classes)


def view_carrega_json_grupos():
    carrega_json('grupos')
    grupos = Grupo.query.all()
    return render_template("grupos.html", grupos=grupos)


def view_carrega_json_materiais():
    carrega_json('materiais')
    materiais = Material.query.all()
    return render_template("materiais.html", materiais=materiais)


def view_carrega_json_pdms():
    carrega_json('pdms')
    pdms = PDM.query.all()
    return render_template("pdms.html", pdms=pdms)
