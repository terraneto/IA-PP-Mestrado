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
    id_orgao_superior = db.Column(db.Integer)
    id_municipio = db.Column(db.Integer)
    cnpj = db.Column(db.String(14))
    cep = db.Column(db.String(8))
    total_fornecedores_cadastrados = db.Column(db.Integer)
    unidade_cadastradora = db.Column(db.Integer)
    ativo = db.Column(db.Integer)


class Orgao(db.Model, SerializerMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    codigo_tipo_adm = db.Column(db.Integer)
    codigo_tipo_esfera = db.Column(db.String(9))
    codigo_tipo_poder = db.Column(db.Integer)
    ativo = db.Column(db.Integer)


class Material(db.Model, SerializerMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    id_grupo = db.Column(db.Integer)
    id_classe = db.Column(db.Integer)
    id_pdm = db.Column(db.Integer)
    status = db.Column(db.Integer)
    sustentavel = db.Column(db.Integer)


class Grupo(db.Model, SerializerMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(130))


class Classe(db.Model, SerializerMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(130))
    codigo_grupo = db.Column(db.Integer)


class PDM(db.Model, SerializerMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(130))
    codigo_classe = db.Column(db.Integer)


class AmbitoOcorrencia(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(25))


class CNAE(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(170))
    codigo_longo = db.Column(db.String(10))


class ComprasContratos(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    codigo_contrato = db.Column(db.String(17))
    numero = db.Column(db.String(12))
    receita_despesa = db.Column(db.String(7))
    orgao_codigo = db.Column(db.Integer)
    orgao_nome = db.Column(db.String(45))
    unidade_codigo = db.Column(db.Integer)
    unidade_nome_resumido = db.Column(db.String(20))
    unidade_nome = db.Column(db.String(50))
    unidade_origem_codigo = db.Column(db.Integer)
    unidade_origem_nome = db.Column(db.String(50))
    codigo_tipo = db.Column(db.Integer)
    tipo = db.Column(db.String(45))
    categoria = db.Column(db.String(25))
    processo = db.Column(db.String(25))
    objeto = db.Column(db.Text)
    fundamento_legal = db.Column(db.String(50))


'''
  `data_assinatura` text, DateTime
  `data_publicacao` text, DateTime
  `vigencia_inicio` text, DateTime
  `vigencia_fim` text,  DateTime
  `valor_inicial` double DEFAULT NULL,
  `valor_global` double DEFAULT NULL,
  `num_parcelas` bigint DEFAULT NULL,
  `valor_parcela` double DEFAULT NULL,
  `valor_acumulado` double DEFAULT NULL,
  `fornecedor_tipo` text,
  `fornecedor_cnpj_cpf_idgener` text,
  `fornecedor_nome` text,
  `codigo_compra` text,
  `modalidade_codigo` text,
  `modalidade` text,
  `unidade_compra` double DEFAULT NULL,
  `licitacao_numero` text,
  `informacao_complementar` text,
 '''
