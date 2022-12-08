from flask import Blueprint

from .views import index, product, view_home, dir_listing, \
    view_baixa_uasgs, uasg, view_carrega_json_uasg, view_baixa_orgaos, view_carrega_json_orgao, \
    view_baixa_tipo_materiais, view_carrega_json_materiais

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

bp.add_url_rule("/json/materiais/<vtipo>", view_func=view_baixa_tipo_materiais, endpoint="view_baixa_tipo_materiais")

bp.add_url_rule("/json/uasgs", view_func=view_baixa_uasgs, endpoint="view_baixa_uasgs")

bp.add_url_rule("/json/Orgaos", view_func=view_baixa_orgaos, endpoint="view_baixa_orgaos")

bp.add_url_rule("/json/uasgs/carregadb", view_func=view_carrega_json_uasg, endpoint="view_carrega_json_uasg")

bp.add_url_rule("/json/orgaos/carregadb", view_func=view_carrega_json_orgao, endpoint="view_carrega_json_orgao")

bp.add_url_rule("/json/materiais/carregadb", view_func=view_carrega_json_materiais,
                endpoint="view_carrega_json_materiais")


def init_app(app):
    app.register_blueprint(bp)
