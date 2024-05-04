from sqlalchemy import ForeignKey

from ppweb.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


class Config(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text)


class Uasg(db.Model, SerializerMixin):
    __tablename__ = "uasg"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(55))
    id_orgao = db.Column(db.Integer)
    id_orgao_superior = db.Column(db.Integer)
    id_municipio = db.Column(db.Integer)
    cnpj = db.Column(db.String(14))
    cep = db.Column(db.String(8))
    total_fornecedores_cadastrados = db.Column(db.Integer)
    total_fornecedores_recadastrados = db.Column(db.Integer)
    unidade_cadastradora = db.Column(db.Integer)
    ativo = db.Column(db.Integer)


class Fornecedor(db.Model, SerializerMixin):
    __tablename__ = "fornecedores"
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.Text)
    cpf = db.Column(db.Text)
    nome = db.Column(db.Text)
    ativo = db.Column(db.Integer)
    recadastrado = db.Column(db.Text)
    id_municipio = db.Column(db.Integer)
    uf = db.Column(db.String(2))
    id_natureza_juridica = db.Column(db.Integer)
    id_porte_empresa = db.Column(db.Integer)
    id_ramo_negocio = db.Column(db.Integer)
    id_unidade_cadastradora = db.Column(db.Text)
    id_cnae = db.Column(db.Integer)
    id_cnae2 = db.Column(db.Integer)
    habilitado_licitar = db.Column(db.Integer)


class Orgao(db.Model, SerializerMixin):
    __tablename__ = "orgao"
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    codigo_tipo_adm = db.Column(db.Integer)
    codigo_tipo_esfera = db.Column(db.String(9))
    codigo_tipo_poder = db.Column(db.Integer)
    ativo = db.Column(db.Integer)


class Material(db.Model, SerializerMixin):
    __tablename__ = "materiais"
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    id_grupo = db.Column(db.Integer)
    id_classe = db.Column(db.Integer)
    id_pdm = db.Column(db.Integer)
    status = db.Column(db.Integer)
    sustentavel = db.Column(db.Integer)


class Grupo(db.Model, SerializerMixin):
    __tablename__ = "grupos"
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(130))


class Classe(db.Model, SerializerMixin):
    __tablename__ = "classes"
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(130))
    codigo_grupo = db.Column(db.Integer)


class PDM(db.Model, SerializerMixin):
    __tablename__ = "pdms"
    codigo = db.Column(db.String(5), primary_key=True)
    descricao = db.Column(db.String(130))
    codigo_classe = db.Column(db.Integer)


class AmbitoOcorrencia(db.Model, SerializerMixin):
    __tablename__ = "ambitos_ocorrencia"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(25))


class CNAE(db.Model, SerializerMixin):
    __tablename__ = "cnaes"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(170))
    codigo_longo = db.Column(db.String(10))


class Municipio(db.Model, SerializerMixin):
    __tablename__ = "municipios"
    id = db.Column(db.Integer, primary_key=True)
    codigo_ibge = db.Column(db.Text)
    nome = db.Column(db.String(45))
    nome_uf = db.Column(db.String(20))
    sigla_uf = db.Column(db.String(2))
    ativo = db.Column(db.Integer)
    capital = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class ComprasContratos(db.Model, SerializerMixin):
    __tablename__ = "comprasContratos"
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
    data_assinatura = db.Column(db.Text)
    data_publicacao = db.Column(db.Text)
    vigencia_inicio = db.Column(db.Text)
    vigencia_fim = db.Column(db.Text)
    valor_inicial = db.Column(db.Float)
    valor_global = db.Column(db.Float)
    num_parcelas = db.Column(db.BigInteger)
    valor_parcela = db.Column(db.Float)
    valor_acumulado = db.Column(db.Float)
    fornecedor_tipo = db.Column(db.Text)
    fornecedor_cnpj_cpf_idgener = db.Column(db.Text)
    fornecedor_nome = db.Column(db.Text)
    codigo_compra = db.Column(db.Text)
    modalidade_codigo = db.Column(db.Text)
    modalidade = db.Column(db.Text)
    unidade_compra = db.Column(db.Float)
    licitacao_numero = db.Column(db.Text)
    informacao_complementar = db.Column(db.Text)


class Licitacao(db.Model, SerializerMixin):
    __tablename__ = "licitacoes"
    uasg = db.Column(db.Integer, primary_key=True)
    modalidade = db.Column(db.Integer, primary_key=True)
    numero_aviso = db.Column(db.Integer, primary_key=True)
    identificador = db.Column(db.Text)
    tipo_pregao = db.Column(db.Text)
    situacao_aviso = db.Column(db.Text)
    objeto = db.Column(db.Text)
    informacoes_gerais = db.Column(db.Text)
    numero_processo = db.Column(db.Text)
    tipo_recurso = db.Column(db.Text)
    numero_itens = db.Column(db.Integer)
    nome_responsavel = db.Column(db.Text)
    funcao_responsavel = db.Column(db.Text)
    data_entrega_edital = db.Column(db.Text)
    endereco_entrega_edital = db.Column(db.Text)
    data_abertura_proposta = db.Column(db.Text)
    data_entrega_proposta = db.Column(db.Text)
    data_publicacao = db.Column(db.Text)


class Itenslicitacao(db.Model, SerializerMixin):
    __tablename__ = "itensLicitacao"
    uasg = db.Column(db.Integer, primary_key=True)
    modalidade = db.Column(db.Integer, primary_key=True)
    numero_aviso = db.Column(db.Integer, primary_key=True)
    numero_licitacao = db.Column(db.Text)
    numero_item_licitacao = db.Column(db.Integer, primary_key=True)
    codigo_item_servico = db.Column(db.Text)
    codigo_item_material = db.Column(db.Integer)
    descricao_item = db.Column(db.Text)
    sustentavel = db.Column(db.Integer)
    quantidade = db.Column(db.Text)
    unidade = db.Column(db.Text)
    cnpj_fornecedor = db.Column(db.Text)
    cpfVencedor = db.Column(db.Text)
    beneficio = db.Column(db.Text)
    valor_estimado = db.Column(db.Float)
    decreto_7174 = db.Column(db.Integer)
    criterio_julgamento = db.Column(db.Text)


class Itenscontratos(db.Model, SerializerMixin):
    __tablename__ = "itensComprasContratos"
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer)
    tipo_id = db.Column(db.Text)
    grupo_id = db.Column(db.Text)
    catmatser_item_id = db.Column(db.Text)
    descricao_complementar = db.Column(db.Text)
    quantidade = db.Column(db.Integer)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)


class Itens(db.Model, SerializerMixin):
    __tablename__ = "itens"
    licitacao_contrato = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    catmat_id = db.Column(db.Integer, ForeignKey(Material.codigo))
    quantidade = db.Column(db.Integer)
    unidade = db.Column(db.Text)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    municipio_uasg = db.Column(db.Integer, ForeignKey(Municipio.id))
    municipio_fornecedor = db.Column(db.Integer, ForeignKey(Municipio.id))
    distancia_uasg_fornecedor = db.Column(db.Float)


class Itensprecospraticados(db.Model, SerializerMixin):
    __tablename__ = "itensPrecoPraticado"
    uasg = db.Column(db.Integer, primary_key=True)
    modalidade = db.Column(db.Integer, primary_key=True)
    numero_aviso = db.Column(db.Integer, primary_key=True)
    numero_item_licitacao = db.Column(db.Integer, primary_key=True)
    codigo_item_material = db.Column(db.Integer)
    codigo_item_servico = db.Column(db.Text)
    cnpj_fornecedor = db.Column(db.Text)
    marca = db.Column(db.Text)
    unidade = db.Column(db.Text)
    quantidade = db.Column(db.Text)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    beneficio = db.Column(db.Text)
    id_licitacao = db.Column(db.Text)


class Pregao(db.Model, SerializerMixin):
    __tablename__ = "pregoes"
    numero = db.Column(db.Integer, primary_key=True)
    co_portaria = db.Column(db.Text)
    dtPortaria = db.Column(db.Text)
    co_processo = db.Column(db.Text)
    ds_tipo_pregao = db.Column(db.Text)
    ds_tipo_pregao_compra = db.Column(db.Text)
    tx_objeto = db.Column(db.Text)
    valorHomologadoTotal = db.Column(db.Float)
    valorEstimadoTotal = db.Column(db.Float)
    co_uasg = db.Column(db.Integer)
    ds_situacao_pregao = db.Column(db.Text)
    dtDataEdital = db.Column(db.Text)
    dtInicioProposta = db.Column(db.Text)
    dtFimProposta = db.Column(db.Text)


class Itempregao(db.Model, SerializerMixin):
    __tablename__ = "itenspregoes"
    id = db.Column(db.Integer, primary_key=True)
    id_pregao = db.Column(db.Integer)
    num_item = db.Column(db.Integer)
    descricao_item = db.Column(db.Text)
    quantidade_item = db.Column(db.Integer)
    valor_estimado_item = db.Column(db.Float)
    descricao_detalhada_item = db.Column(db.Text)
    tratamento_diferenciado = db.Column(db.Text)
    decreto_7174 = db.Column(db.Integer)
    margem_preferencial = db.Column(db.Integer)
    unidade_fornecimento = db.Column(db.Text)
    situacao_item = db.Column(db.Text)
    fornecedor_vencedor = db.Column(db.Text)
    menor_lance = db.Column(db.Float)
    valorHomologadoItem = db.Column(db.Float)
    valor_negociado = db.Column(db.Float)


class Itenscompletos(db.Model, SerializerMixin):
    __tablename__ = "itenscompletos"
    licitacao_contrato = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    catmat_id = db.Column(db.Integer, ForeignKey(Material.codigo))
    quantidade = db.Column(db.Integer)
    unidade = db.Column(db.Text)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    municipio_uasg = db.Column(db.Integer, ForeignKey(Municipio.id))
    municipio_fornecedor = db.Column(db.Integer, ForeignKey(Municipio.id))
    distancia_uasg_fornecedor = db.Column(db.Float)
    tipo = db.Column(db.Text)
    uasg = db.Column(db.Text)
    fornecedor_cpfcnpj = db.Column(db.Text)
    fornecedor_nome = db.Column(db.Text)
    numero = db.Column(db.Text)
