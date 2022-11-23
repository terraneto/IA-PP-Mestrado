from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator, Link

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
        'IAPP',
        View('Home', 'webui.index'),
        View('Produto', 'webui.index'),
        View('Outro', 'webui.view_home'),
        Subgroup('subpáginas',
                 View('firstpage', 'webui.firstpage'),
                 Separator(),
                 View('secondpage', 'webui.secondpage'),
                 ),
        Link('Tech Support', 'http://www.google.com'),
    )


def init_app(app):
    nav.init_app(app)
