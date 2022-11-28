from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator, Link, Text

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
                 View('Carregar Jsons', 'webui.view_carrega_json_uasg'),
                 View('Baixar Jsons', 'webui.view_baixa_uasgs')
                 ),
#        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
