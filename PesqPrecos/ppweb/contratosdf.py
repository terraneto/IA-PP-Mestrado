from ppweb.ext.database import db

from ppweb.models import ComprasContratos


def create_contratos_from_dataframe(df):
    print(df)
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            contrato = ComprasContratos()
            contrato.id = df_classe['id']
            contrato.codigo_contrato = df_classe['codigo_contrato']
            contrato.numero = df_classe['numero']
            contrato.receita_despesa = df_classe['receita_despesa']
            contrato.orgao_codigo = df_classe['orgao_codigo']
            contrato.orgao_nome = df_classe['orgao_nome']
            contrato.unidade_codigo = df_classe['unidade_codigo']
            contrato.unidade_nome_resumido = df_classe['unidade_nome_resumido']
            contrato.unidade_nome = df_classe['unidade_nome']
            contrato.unidade_origem_codigo = df_classe['unidade_origem_codigo']
            contrato.unidade_origem_nome = df_classe['unidade_origem_nome']
            exists = db.session.query(db.exists().where(ComprasContratos.id == df_classe['id'])).scalar()
            if exists:
                print(contrato)
                contrato.verified = True
            else:
                db.session.add(contrato)
            print(contrato)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


"""
    codigo_tipo = db.Column(db.Integer)
    tipo = db.Column(db.String(45))
    categoria = db.Column(db.String(25))
    processo = db.Column(db.String(25))
    objeto = db.Column(db.Text)
    fundamento_legal = db.Column(db.String(50))
    data_assinatura = db.Column(db.DateTime)
    data_publicacao = db.Column(db.DateTime)
    vigencia_inicio = db.Column(db.DateTime)
    vigencia_fim = db.Column(db.DateTime)
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
"""
