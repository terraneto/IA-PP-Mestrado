from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator

# , Link

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
        'IAPP',
        View('Home', 'webui.index'),
        View('Produto', 'webui.index'),
        Subgroup('Outro',
                 View('Outro', 'webui.view_home'),
                 View('Seleciona tipo', 'webui.view_seltipo'),
                 ),
        Subgroup('UASG',
                 View('Uasgs', 'webui.uasg'),
                 View('Listar Jsons', 'webui.jsonpath', req_path='uasgs'),
                 ),
        Subgroup('Baixar Jsons',
                 Text('Módulo Contratos desde 2021'),
                 View('Contratos', 'webui.view_baixa_json_contratos_mensal', vmodulo='compraContratos',
                      vtipo='contratos', vano=2022),
                 Separator(),
                 Text('Módulo Fornecedores'),
                 View('Âmbitos de Ocorrência', 'webui.view_baixa_json', vmodulo='fornecedores',
                      vtipo='ambitos_ocorrencia'),
                 View('CNAEs', 'webui.view_baixa_json', vmodulo='fornecedores',
                      vtipo='cnaes'),
                 View('Municípios', 'webui.view_baixa_json', vmodulo='fornecedores',
                      vtipo='municipios'),
                 Separator(),
                 Text('Módulo Materiais'),
                 View('Classes', 'webui.view_baixa_json', vmodulo='materiais', vtipo='classes'),
                 View('Grupos', 'webui.view_baixa_json', vmodulo='materiais', vtipo='grupos'),
                 View('Materiais', 'webui.view_baixa_json', vmodulo='materiais', vtipo='materiais'),
                 View('PDMs', 'webui.view_baixa_json', vmodulo='materiais', vtipo='pdms'),
                 View('Material por Id', 'webui.view_baixa_material_por_id'),
                 Separator(),
                 Text('Módulo Licitações'),
                 View('Licitações', 'webui.view_baixa_json_diario', vmodulo='licitacoes', vtipo='licitacoes',
                      vano=2022),
                 View('Modalidade de Licitações', 'webui.view_baixa_json', vmodulo='licitacoes',
                      vtipo='modalidades_licitacao'),
                 View('Órgãos', 'webui.view_baixa_json', vmodulo='licitacoes', vtipo='orgaos'),
                 View('Uasgs', 'webui.view_baixa_json', vmodulo='licitacoes', vtipo='uasgs'),
                 ),
        Subgroup('Carregar Jsons',
                 Text('Módulo Fornecedores'),
                 Separator(),
                 Text('Módulo Materiais'),
                 View('Classes', 'webui.view_carrega_json_classes'),
                 View('Grupos', 'webui.view_carrega_json_grupos'),
                 View('Materiais', 'webui.view_carrega_json_materiais'),
                 View('PDMs', 'webui.view_carrega_json_pdms'),
                 Separator(),
                 Text('Módulo Licitações'),
                 View('Órgãos', 'webui.view_carrega_json_orgao'),
                 View('Uasgs', 'webui.view_carrega_json_uasg'),
                 ),

        #        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
