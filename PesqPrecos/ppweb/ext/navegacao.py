import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator


# , Link

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
        'IAPP',
        View('Home', 'webui.index'),
        Subgroup('Listagens',
                 Text('Módulo Contratos desde 2021'),
                 View('Itens dos Contratos', 'webui.view_itenscontratos'),
                 Separator(),
                 View('Uasgs', 'webui.uasg'),
                 View('Listar Jsons', 'webui.jsonpath', req_path='uasgs'),
                 ),
        Subgroup('Preparação do Repositório',
                 Separator(),
                 Text('Baixar Jsons'),
                 View('Baixar Json selecionando tipo', 'webui.view_seltipo'),
                 View('Baixar Jsons de Licitações', 'webui.view_licitacoesseltipo'),
                 Separator(),
                 Text('Carregar Jsons no Banco'),
                 View('Carregar Jsons do tipo selecionado', 'webui.view_cargaseltipo'),
                 Separator(),
                 Text('Módulo Contratos desde 2021'),
                 View('Contratos 2023', 'webui.view_baixa_json_contrato_mensal', vano=2023),
                 View('Contratos do ano 2023', 'webui.view_baixa_json_contrato_anual', vano=2023),
                 View('Contratos do mês', 'webui.view_baixa_json_contrato_mes', vano=2023, vmes='04'),
                 View('Itens dos Contratos', 'webui.view_baixa_json_itenscontrato'),
                 View('Carregar json de Contratos', 'webui.view_carrega_json_contratos_mensais'),
                 View('Carregar json de Itens dos Contratos', 'webui.view_carrega_json_itenscontratos')
                 ),
        Subgroup('Licitações',
                 View('Itens das licitações', 'webui.view_baixa_json_itenslicitacao'),
                 View('Licitações do mês', 'webui.view_baixa_json_licitacoes_mes', vano=2022, vmes=12),
                 View('Licitações mensais', 'webui.view_baixa_json_licitacao_uasg_mensal', vano=2022, vmes=12),
                 View('Preços praticados', 'webui.view_baixa_json_itensprecospraticados'),
                 ),
        Subgroup('Preparação de Dados',
                 Text('Módulo Contratos desde 2021'),
                 View('Carrega itens de contratos de material', 'webui.view_carrega_itens_contratos'),
                 Text('Licitações'),
                 View('Carrega itens de preços praticados', 'webui.view_carrega_itens_licitacoes'),
                 ),

        #        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
