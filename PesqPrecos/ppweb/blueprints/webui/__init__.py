from flask import Blueprint

from .views import index, product, view_home, view_second_page, view_first_page

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule(
    "/product/<product_id>", view_func=product, endpoint="productview"
)
bp.add_url_rule(
    "/home", view_func=view_home, endpoint="view_home"
)
bp.add_url_rule(
    "/firstpage", view_func=view_first_page, endpoint="firstpage"
)
bp.add_url_rule(
    "/secondpage", view_func=view_second_page, endpoint="secondpage"
)


def init_app(app):
    app.register_blueprint(bp)
