from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator
import collections.abc
import collections

collections.MutableMapping = collections.abc.MutableMapping


# , Link

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
        'IAPP',
        # View('Home', 'webui.index'),
        # Subgroup('Listagens',
        #         Text('Módulo Contratos desde 2021'),
        #         View('Itens dos Contratos', 'webui.view_itenscontratos'),
        #         Separator(),
        #         View('Uasgs', 'webui.uasg'),
        #         View('Listar Jsons', 'webui.jsonpath', req_path='uasgs'),
        #         ),
        Subgroup('Obtenção de dados',
                 Separator(),
                 Text('Baixar Jsons'),
                 View('Selecionando tipo', 'webui.view_seltipo'),
                 View('Licitações', 'webui.view_licitacoesseltipo'),
                 View('Itens das licitações', 'webui.view_baixa_json_itenslicitacao'),
                 View('Preços praticados', 'webui.view_baixa_json_itensprecospraticados'),
                 View('Pregões', 'webui.view_baixa_json_pregoes'),
                 View('Itens de pregão', 'webui.view_baixa_json_itens_pregoes'),
                 View('Contratos', 'webui.view_contratosseltipo'),
                 View('Contratos do ano baixados mensalmente', 'webui.view_contratosselano'),
                 View('Itens dos Contratos', 'webui.view_baixa_json_itenscontrato'),
                 Separator(),
                 Text('Carregar Jsons no Banco'),
                 View('Tipo selecionado', 'webui.view_cargaseltipo'),
                 View('Licitações por ano', 'webui.view_cargalicitacaoano'),
                 View('Pregões', 'webui.view_carrega_json_pregoes'),
                 View('Itens dos Pregões', 'webui.view_carrega_json_itenspregoes'),
                 View('Contratos', 'webui.view_carrega_json_contratos_mensais'),
                 View('Itens dos Contratos', 'webui.view_carrega_json_itenscontratos')
                 ),
        # Subgroup('Licitações',
        #         View('Licitações do mês', 'webui.view_baixa_json_licitacoes_mes', vano=2022, vmes=12),
        #         View('Licitações mensais', 'webui.view_baixa_json_licitacao_uasg_mensal', vano=2022, vmes=12),
        #         ),
        Subgroup('Preparação do Repositório',
                 Text('Módulo Contratos desde 2021'),
                 View('Carrega itens de contratos de material', 'webui.view_carrega_itens_contratos'),
                 Text('Licitações'),
                 View('Carrega itens de preços praticados', 'webui.view_carrega_itens_licitacoes'),
                 Text('Correções'),
                 View('Corrige cálculo da distância entre uasg e fornecedor', 'webui.view_corrige_distancia'),
                 ),
        Subgroup('Avaliação da Pesquisa de Preços',
                 View('Avalia pesquisa de preços', 'webui.view_avalia_pesquisa_precos')
                 ),
        #        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
