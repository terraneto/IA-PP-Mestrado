from flask import Blueprint

from .views import index, product, view_home, dir_listing, \
    uasg, view_carrega_json_uasg, view_carrega_json_orgao, \
    view_carrega_json_materiais, view_baixa_json, view_carrega_json_classes, view_carrega_json_grupos, \
    view_carrega_json_pdms, view_seltipo, view_baixa_json_contratos_mensal, update_dropdown, process_data, \
    view_baixa_json_diario, view_carrega_json_cnaes, \
    view_carrega_json_ambitos_ocorrencia, view_carrega_json_municipios, view_carrega_json_contratos_mensais

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)

bp.add_url_rule("/uasgs", view_func=uasg)

bp.add_url_rule(
    "/product/<product_id>", view_func=product, endpoint="productview"
)

bp.add_url_rule(
    "/home", view_func=view_home, endpoint="view_home"
)

bp.add_url_rule("/json", view_func=dir_listing, endpoint="json")

bp.add_url_rule("/json/<req_path>", view_func=dir_listing, endpoint="jsonpath")

bp.add_url_rule("/json/<vmodulo>/<vtipo>", view_func=view_baixa_json, endpoint="view_baixa_json")

bp.add_url_rule("/json/<vmodulo>/<vtipo>/<vano>/diario", view_func=view_baixa_json_diario,
                endpoint="view_baixa_json_diario")

bp.add_url_rule("/json/<vmodulo>/<vtipo>/<vano>", view_func=view_baixa_json_contratos_mensal,
                endpoint="view_baixa_json_contratos_mensal")

bp.add_url_rule("/json/uasgs/carregadb", view_func=view_carrega_json_uasg, endpoint="view_carrega_json_uasg")

bp.add_url_rule("/json/orgaos/carregadb", view_func=view_carrega_json_orgao, endpoint="view_carrega_json_orgao")

bp.add_url_rule("/carregadb/classes", view_func=view_carrega_json_classes,
                endpoint="view_carrega_json_classes")

bp.add_url_rule("/carregadb/grupos", view_func=view_carrega_json_grupos,
                endpoint="view_carrega_json_grupos")

bp.add_url_rule("/carregadb/materiais", view_func=view_carrega_json_materiais,
                endpoint="view_carrega_json_materiais")

bp.add_url_rule("/carregadb/municipios", view_func=view_carrega_json_municipios,
                endpoint="view_carrega_json_municipios")

bp.add_url_rule("/carregadb/pdms", view_func=view_carrega_json_pdms,
                endpoint="view_carrega_json_pdms")

bp.add_url_rule("/carregadb/ambitos_ocorrencia", view_func=view_carrega_json_ambitos_ocorrencia,
                endpoint="view_carrega_json_ambitos_ocorrencia")

bp.add_url_rule("/carregadb/contratos", view_func=view_carrega_json_contratos_mensais,
                endpoint="view_carrega_json_contratos_mensais")

bp.add_url_rule("/carregadb/cnaes", view_func=view_carrega_json_cnaes,
                endpoint="view_carrega_json_cnaes")

bp.add_url_rule("/seltipo", view_func=view_seltipo,
                endpoint="view_seltipo")

bp.add_url_rule("/_update_dropdown", view_func=update_dropdown,
                endpoint="update_dropdown")
bp.add_url_rule("/_process_data", view_func=process_data,
                endpoint="process_data")


def init_app(app):
    app.register_blueprint(bp)
