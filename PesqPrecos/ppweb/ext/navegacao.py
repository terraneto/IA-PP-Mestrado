from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

# , Separator, Link, Text

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
        'IAPP',
        View('Home', 'webui.index'),
        View('Produto', 'webui.index'),
        View('Outro', 'webui.view_home'),
        Subgroup('UASG',
                 View('Uasgs', 'webui.uasg'),
                 View('Listar Jsons', 'webui.jsonpath', req_path='uasgs'),
                 #                 Separator(),
                 #                 Text('Teste de texto'),

                 ),
        Subgroup('Baixar Jsons',
                 View('Classes', 'webui.view_baixa_tipo_materiais', vtipo='classes'),
                 View('Grupos', 'webui.view_baixa_tipo_materiais', vtipo='grupos'),
                 View('Materiais', 'webui.view_baixa_tipo_materiais', vtipo='materiais'),
                 View('Órgãos', 'webui.view_baixa_orgaos'),
                 View('PDMs', 'webui.view_baixa_tipo_materiais', vtipo='pdms'),
                 View('Uasgs', 'webui.view_baixa_uasgs'),
                 ),
        Subgroup('Carregar Jsons',
                 View('Materiais', 'webui.view_carrega_json_materiais'),
                 View('Órgãos', 'webui.view_carrega_json_orgao'),
                 View('Uasgs', 'webui.view_carrega_json_uasg'),
                 ),

        #        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
