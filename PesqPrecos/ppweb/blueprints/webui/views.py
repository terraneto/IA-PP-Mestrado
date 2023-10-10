from datetime import datetime, timedelta, date
from flask import abort, render_template, send_file, request, jsonify
from ppweb.cargajson import carrega_json

from ppweb.contratosdf import baixa_json_contrato_mensal, baixa_json_itenscontrato, baixa_json_contrato_anual, \
    baixa_json_contrato_mes
from ppweb.dadosia import carrega_itens_contratos, carrega_itens_licitacoes
from ppweb.ext.database import db
from ppweb.ia import recuperar_itens_catmat, retirar_extremos, treina_modelo, avalia_dados
from ppweb.licitacoesdf import baixa_json_itenslicitacao, \
    baixa_json_uasg_licitacoes_mensal, baixa_json_licitacao_uasg_mensal, baixa_json_licitacao_uasg_trimestral, \
    baixa_json_itensprecospraticados, baixa_json_licitacao_uasg_anual_geral, baixa_uasg_diario_material_geral, \
    baixa_uasg_mensal_geral, baixa_uasg_mensal_diario_geral, baixa_uasg_diario_classe_geral

from ppweb.models import Uasg, ComprasContratos, Itenslicitacao, Itenscontratos, Itens, Itensprecospraticados, Material

import os

from ppweb.utils import baixa_json


def index():
    return render_template("index.html")


def get_dropdown_values():
    modulos = {
        'fornecedores': ['ambitos_ocorrencia', 'cnaes', 'fornecedores', 'linhas_fornecimento', 'municipios',
                         'naturezas_juridicas', 'ocorrencias_fornecedores', 'portes_empresa', 'prazos_ocorrencia',
                         'ramos_negocio', 'tipos_ocorrencia'],
        'materiais': ['classes', 'grupos', 'pdms', 'materiais'],
        'licitacoes': ['modalidades_licitacao', 'orgaos', 'uasgs']
    }
    return modulos


def get_carga_values():
    modulos = {'ambitos_ocorrencia', 'cnaes', 'fornecedores', 'linhas_fornecimento', 'municipios',
               'naturezas_juridicas', 'ocorrencias_fornecedores', 'portes_empresa', 'prazos_ocorrencia',
               'ramos_negocio', 'tipos_ocorrencia', 'classes', 'grupos', 'pdms', 'materiais',
               'modalidades_licitacao', 'orgaos', 'uasgs', 'licitacoes', 'itenslicitacao',
               'itensprecospraticados'
               }
    return modulos


def update_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)
    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]
    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
    return jsonify(html_string_selected=html_string_selected)


def selecao_material():
    material_selecionado = request.args.get('material_selecionado', type=int)
    material = Material.query.filter_by(codigo=material_selecionado).first()
    retorno = material.to_dict()
    print(retorno)
    return retorno


def avaliacao_pp():
    if request.method == 'POST':
        material_selecionado = request.form.get('all_materiais', type=int)
        data_selecionada = request.form.get('data_selecionada', type=str)
    else:
        material_selecionado = request.args.get('material_selecionado', type=int)
        data_selecionada = request.args.get('data_selecionada', type=str)
    material = Material.query.filter_by(codigo=material_selecionado).first()
    dataformatada = date.fromisoformat(data_selecionada).strftime('%d/%m/%Y')
    df = recuperar_itens_catmat(material_selecionado, data_selecionada)
    df = retirar_extremos(df)
    min = "{:.2f}".format(df['valor_unitario'].min())
    min = f"\t{min.replace('.', ',')}"
    max = "{:.2f}".format(df['valor_unitario'].max())
    max = f"\t{max.replace('.', ',')}"
    media = "{:.2f}".format(df['valor_unitario'].mean())
    media = f"\t{media.replace('.', ',')}"
    mediana = "{:.2f}".format(df['valor_unitario'].median())
    mediana = f"\t{mediana.replace('.', ',')}"
    qmin = f"\t{str(df['quantidade'].min()).replace('.', ',')}"
    qmax = f"\t{str(df['quantidade'].max()).replace('.', ',')}"
    qmedia = "{:.2f}".format(df['quantidade'].mean())
    qmedia = f"\t{qmedia.replace('.', ',')}"
    qmediana = "{:.2f}".format(df['quantidade'].median())
    qmediana = f"\t{qmediana.replace('.', ',')}"
    return render_template("avaliacao_pesquisa.html", material=material, datainicio=dataformatada, min=min, max=max,
                           media=media, qmin=qmin, qmax=qmax, qmedia=qmedia, qmediana=qmediana, numreg=len(df),
                           mediana=mediana)


def testa_sobrepreco():
    try:
        quantidade = request.args.get('qtd', type=int)
        valor = request.args.get('valor', type=str)
        valor = float(f"\t{valor.replace(',', '.')}")
        catmat = request.args.get('catmat', type=int)
        datainicio = request.args.get('datainicio', type=str)
        print(datainicio)
        df = recuperar_itens_catmat(catmat, datainicio)
        mediana = df['valor_unitario'].median()
        minimo = df['valor_unitario'].min()
        if valor < minimo:
            qmax = df['quantidade'].max()
            if quantidade < qmax:
                retorno = {'predicao': 'Possibilidade de preço inexequivel'}
            else:
                retorno = {'predicao': 'Valor aceitável'}
        else:
            if valor <= mediana:
                retorno = {'predicao': 'Valor aceitável'}
            else:
                clf = treina_modelo(df, 0.1)
                predicao = int(avalia_dados(clf, quantidade, valor))
                if predicao == 0:
                    retorno = {'predicao': 'Valor aceitável'}
                else:
                    retorno = {'predicao': 'Possibilidade de sobrepreço'}
    except:
        retorno = {'predicao': 'Parâmetros inválidos ou erro no cálculo'}
    return retorno


def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    baixa_json(selected_class, selected_entry, None)
    return dir_listing(selected_entry)


def process_data_licitacao():
    if request.method == 'POST':
        result = request.form
        ano = result.get('select_ano')
        inicio = result.get('select_inicio')
        recursivo = result.get('recursividade')
        sobrepoe = result.get('sobrepoe')
        print(ano)
        print(inicio)
        print(recursivo)
        print(sobrepoe)
        if ano == '3':
            baixa_json_licitacao_uasg_trimestral()
        else:
            match inicio:
                case '1':
                    baixa_json_licitacao_uasg_anual_geral(ano, recursivo)
                case '2':
                    baixa_uasg_mensal_geral(ano, recursivo)
                case '3':
                    baixa_uasg_mensal_diario_geral(ano, recursivo)
                case '4':
                    baixa_uasg_diario_classe_geral(ano, recursivo)
                case '5':
                    baixa_uasg_diario_material_geral(ano)
    return dir_listing('licitacoes')


def carrega_dados():
    selected_class = request.args.get('selected_class', type=str)
    carrega_json(selected_class)
    return dir_listing(selected_class)


def view_seltipo():
    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    return render_template('seltipo.html',
                           all_classes=default_classes,
                           all_entries=default_values)


def view_avalia_pesquisa_precos():
    ontem = (datetime.now() - timedelta(30)).strftime('%Y-%m-%d')
    anopassado = (datetime.now() - timedelta(365)).strftime('%Y-%m-%d')
    anopassado = '2022-01-01'
    sql = 'select  itens2.catmat_id as catmat_id, count(*) as qtd, materiais.descricao   from itens2  inner join ' \
          'materiais on itens2.catmat_id = materiais.codigo group by catmat_id order by qtd desc'
    materiais = db.engine.execute(sql).all()
    materiaisfiltrados = [materiais for materiais in materiais if materiais['qtd'] > 30]
    material = materiaisfiltrados[0]
    return render_template('avaliapp.html',
                           all_materiais=materiaisfiltrados, material=material, ontem=ontem, anopassado=anopassado)


def view_licitacoesseltipo():
    return render_template('licitacoesseltipo.html')


def view_cargaseltipo():
    class_entry_relations = get_carga_values()
    default_classes = sorted(class_entry_relations)
    return render_template('cargaseltipo.html',
                           all_classes=default_classes)


def view_carrega_dados(tipo):
    print("carrega dados - " + tipo)
    carrega_json(tipo)
    return dir_listing(tipo)


def uasg():
    uasgs = Uasg.query.all()
    return render_template("uasgs.html", uasgs=uasgs)


# def product(product_id):
#    product = Product.query.filter_by(id=product_id).first() or abort(
#        404, "produto nao encontrado"
#    )
#    return render_template("product.html", product=product)

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


def view_baixa_json_contrato_mensal(vano):
    baixa_json_contrato_mensal(vano)
    return dir_listing("contratos")


def view_baixa_json_contrato_anual(vano):
    baixa_json_contrato_anual(vano)
    return dir_listing("contratos")


def view_baixa_json_contrato_mes(vano, vmes):
    baixa_json_contrato_mes(vano, vmes)
    return dir_listing("contratos")


def view_baixa_json_licitacao_uasg_mensal(vano, vmes):
    print('view baixa licitacoes  Menasl=' + str(vano) + str(vmes))
    baixa_json_licitacao_uasg_mensal(vano, vmes)
    return dir_listing('licitacoes')


def view_baixa_json_itenslicitacao():
    print('view baixa itens da licitacao')
    baixa_json_itenslicitacao()
    return dir_listing('itenslicitacao')


def view_baixa_json_itensprecospraticados():
    print('view baixa itens de preços praticados')
    baixa_json_itensprecospraticados()
    return dir_listing('itensprecospraticados')


def view_baixa_json_licitacoes_mes(vano, vmes):
    baixa_json_uasg_licitacoes_mensal(vano, vmes)
    return dir_listing('licitacoes')


def view_baixa_json_itenscontrato():
    print('view baixa itens do contrato')
    baixa_json_itenscontrato()
    return dir_listing('itenscontrato')


def view_carrega_json_contratos_mensais():
    carrega_json('contratos')
    contratos = ComprasContratos.query.all()
    return render_template("contratos.html", contratos=contratos)


def view_carrega_json(tipo):
    carrega_json(tipo)


def view_carrega_json_itenscontratos():
    carrega_json('itenscontrato')
    itenscontrato = Itenscontratos.query.all()
    return render_template("itenscontratos.html", itenscontrato=itenscontrato)


def view_itenscontratos():
    itenscontrato = Itenscontratos.query.all()
    return render_template("itenscontratos.html", itenscontrato=itenscontrato)


def view_itens():
    itens = Itens.query.all()
    return render_template("itens.html", itens=itens)


def view_carrega_itens_contratos():
    carrega_itens_contratos()
    itens = Itens.query.all()
    return render_template("itens.html", itens=itens)


def view_carrega_itens_licitacoes():
    carrega_itens_licitacoes()
    itens = Itens.query.all()
    return render_template("itens.html", itens=itens)
