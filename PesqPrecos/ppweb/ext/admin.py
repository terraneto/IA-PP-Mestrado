from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from flask_simplelogin import login_required
from werkzeug.security import generate_password_hash

from ppweb.ext.database import db
from ppweb.models import User, Uasg, Config, Orgao, Classe, Material, Grupo, PDM, CNAE, AmbitoOcorrencia, \
    ComprasContratos, Licitacao, Itenslicitacao, Itenscontratos, Itensprecospraticados, Itens

# Proteger o admin com login via Monkey Patch
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()


class UserAdmin(sqla.ModelView):
    column_list = ['username']
    can_edit = False

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)


def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(sqla.ModelView(Uasg, db.session))
    admin.add_view(sqla.ModelView(Orgao, db.session))
    admin.add_view(sqla.ModelView(Classe, db.session))
    admin.add_view(sqla.ModelView(Material, db.session))
    admin.add_view(sqla.ModelView(Grupo, db.session))
    admin.add_view(sqla.ModelView(PDM, db.session))
    admin.add_view(sqla.ModelView(CNAE, db.session))
    admin.add_view(sqla.ModelView(AmbitoOcorrencia, db.session))
    admin.add_view(sqla.ModelView(ComprasContratos, db.session))
    admin.add_view(sqla.ModelView(Licitacao, db.session))
    admin.add_view(sqla.ModelView(Itenslicitacao, db.session))
    admin.add_view(sqla.ModelView(Itenscontratos, db.session))
    admin.add_view(sqla.ModelView(Itensprecospraticados, db.session))
    admin.add_view(sqla.ModelView(Itens, db.session))
    admin.add_view(sqla.ModelView(Config, db.session))
    admin.add_view(UserAdmin(User, db.session))
