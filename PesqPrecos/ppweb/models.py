from ppweb.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


class Config(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text)


class Uasg(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(55))
    id_orgao = db.Column(db.Integer)
    id_municipio = db.Column(db.Integer)
    cnpj = db.Column(db.String(14))
    cep = db.Column(db.String(8))
    total_fornecedores_cadastrados = db.Column(db.Integer)
    total_fornecedores_recadastrados = db.Column(db.Integer)
    unidade_cadastradora = db.Column(db.Integer)
    ativo = db.Column(db.Integer)




