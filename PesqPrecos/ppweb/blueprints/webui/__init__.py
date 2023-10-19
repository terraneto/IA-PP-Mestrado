from flask import Blueprint

from .views import index, dir_listing, \
    uasg, view_baixa_json, view_seltipo, update_dropdown, process_data, \
    view_carrega_json_contratos_mensais, \
    view_baixa_json_itenslicitacao, view_baixa_json_itenscontrato, view_baixa_json_licitacoes_mes, \
    view_carrega_json_itenscontratos, view_baixa_json_contrato_mensal, \
    view_baixa_json_contrato_anual, view_baixa_json_contrato_mes, \
    view_baixa_json_licitacao_uasg_mensal, view_itenscontratos, view_itens, view_carrega_itens_contratos, \
    view_baixa_json_itensprecospraticados, view_carrega_itens_licitacoes, \
    view_cargaseltipo, view_carrega_dados, carrega_dados, view_licitacoesseltipo, \
    process_data_licitacao, view_avalia_pesquisa_precos, selecao_material, avaliacao_pp, testa_sobrepreco, \
    view_cargalicitacaoano, process_ano_licitacao, view_baixa_json_pregoes, view_carrega_json_pregoes, \
    view_baixa_json_itens_pregoes, view_carrega_json_itenspregoes

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)

bp.add_url_rule("/uasgs", view_func=uasg)

# bp.add_url_rule(
#    "/product/<product_id>", view_func=product, endpoint="productview"
# )


# 3bp.add_url_rule(
#    "/home", view_func=view_home, endpoint="view_home"
# )

bp.add_url_rule("/json", view_func=dir_listing, endpoint="json")

bp.add_url_rule("/json/<req_path>", view_func=dir_listing, endpoint="jsonpath")

bp.add_url_rule("/json/<vmodulo>/<vtipo>", view_func=view_baixa_json, endpoint="view_baixa_json")

bp.add_url_rule("/json/pregoes/pregao", view_func=view_baixa_json_pregoes, endpoint="view_baixa_json_pregoes")

bp.add_url_rule("/json/pregoes/itens", view_func=view_baixa_json_itens_pregoes, endpoint="view_baixa_json_itens_pregoes")

bp.add_url_rule("/json/comprascontratos/<vano>", view_func=view_baixa_json_contrato_mensal,
                endpoint="view_baixa_json_contrato_mensal")

bp.add_url_rule("/json/comprascontratos/anual/<vano>", view_func=view_baixa_json_contrato_anual,
                endpoint="view_baixa_json_contrato_anual")

bp.add_url_rule("/json/comprascontratos/ano/<vano>/mes/<vmes>", view_func=view_baixa_json_contrato_mes,
                endpoint="view_baixa_json_contrato_mes")

bp.add_url_rule("/json/itenslicitacao", view_func=view_baixa_json_itenslicitacao,
                endpoint="view_baixa_json_itenslicitacao")

bp.add_url_rule("/json/itensprecospraticados", view_func=view_baixa_json_itensprecospraticados,
                endpoint="view_baixa_json_itensprecospraticados")

bp.add_url_rule("/json/licitacoes/ano/<vano>/mes/<vmes>", view_func=view_baixa_json_licitacoes_mes,
                endpoint="view_baixa_json_licitacoes_mes")

bp.add_url_rule("/json/itenscontrato", view_func=view_baixa_json_itenscontrato,
                endpoint="view_baixa_json_itenscontrato")

bp.add_url_rule("/json/uasg/licitacao/mensal/<vano>/<vmes>", view_func=view_baixa_json_licitacao_uasg_mensal,
                endpoint="view_baixa_json_licitacao_uasg_mensal")

bp.add_url_rule("/carregadb/contratos", view_func=view_carrega_json_contratos_mensais,
                endpoint="view_carrega_json_contratos_mensais")

bp.add_url_rule("/carregadb/itenscontratos", view_func=view_carrega_json_itenscontratos,
                endpoint="view_carrega_json_itenscontratos")

bp.add_url_rule("/carregadb/pregoes", view_func=view_carrega_json_pregoes,
                endpoint="view_carrega_json_pregoes")

bp.add_url_rule("/carregadb/itenspregoes", view_func=view_carrega_json_itenspregoes,
                endpoint="view_carrega_json_itenspregoes")

bp.add_url_rule("/seltipo", view_func=view_seltipo,
                endpoint="view_seltipo")

bp.add_url_rule("/cargaseltipo", view_func=view_cargaseltipo,
                endpoint="view_cargaseltipo")

bp.add_url_rule("/cargalicitacaoano", view_func=view_cargalicitacaoano,
                endpoint="view_cargalicitacaoano")

bp.add_url_rule("/licitacoesseltipo", view_func=view_licitacoesseltipo,
                endpoint="view_licitacoesseltipo")

bp.add_url_rule("/carrega_dados/<tipo>", view_func=view_carrega_dados,
                endpoint="view_carrega_dados")

bp.add_url_rule("/itenscontratos", view_func=view_itenscontratos,
                endpoint="view_itenscontratos")

bp.add_url_rule("/itensdecontratos", view_func=view_carrega_itens_contratos,
                endpoint="view_carrega_itens_contratos")

bp.add_url_rule("/itensdelicitacoes", view_func=view_carrega_itens_licitacoes,
                endpoint="view_carrega_itens_licitacoes")

bp.add_url_rule("/_update_dropdown", view_func=update_dropdown,
                endpoint="update_dropdown")
bp.add_url_rule("/_process_data", view_func=process_data,
                endpoint="process_data")

bp.add_url_rule("/_process_data_licitacao", view_func=process_data_licitacao, endpoint="process_data_licitacoes",
                methods=['POST'])

bp.add_url_rule("/_process_ano_licitacao", view_func=process_ano_licitacao, endpoint="process_ano_licitacoes",
                methods=['POST'])

bp.add_url_rule("/_carrega_dados", view_func=carrega_dados,
                endpoint="carrega_dados")

bp.add_url_rule("/avalia_pp", view_func=view_avalia_pesquisa_precos,
                endpoint="view_avalia_pesquisa_precos")

bp.add_url_rule("/_selecao_material", view_func=selecao_material,
                endpoint="selecao_material")

bp.add_url_rule("/_avaliacao_pp", view_func=avaliacao_pp,
                endpoint="avaliacao_pp", methods=['GET', 'POST'])

bp.add_url_rule("/_testa_sobrepreco", view_func=testa_sobrepreco,
                endpoint="testa_sobrepreco")

def init_app(app):
    app.register_blueprint(bp)
