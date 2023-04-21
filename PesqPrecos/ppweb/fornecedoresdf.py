from ppweb.ext.database import db

from ppweb.models import AmbitoOcorrencia, CNAE, Municipio, Fornecedor


def create_ambitos_ocorrencia_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            ambitoocorrencia = AmbitoOcorrencia.query.filter_by(id=df_classe['id']).first()
            if ambitoocorrencia is None:
                exists = False
                ambitoocorrencia = AmbitoOcorrencia()
            else:
                exists = True
            ambitoocorrencia.id = df_classe['id']
            ambitoocorrencia.descricao = df_classe['descricao']
            if exists:
                ambitoocorrencia.verified = True
            else:
                db.session.add(ambitoocorrencia)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_cnaes_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            cnae = CNAE.query.filter_by(id=df_classe['id']).first()
            if cnae is None:
                exists = False
                cnae = CNAE()
            else:
                exists = True
            cnae.id = df_classe['id']
            cnae.descricao = df_classe['descricao']
            cnae.codigo_longo = df_classe['codigo_longo']
            if exists:
                cnae.verified = True
            else:
                db.session.add(cnae)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        print(excecao.__traceback__)


def create_municipios_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            municipio = Municipio.query.filter_by(id=df_classe['id']).first()
            if municipio is None:
                exists = False
                municipio = Municipio()
            else:
                exists = True
            municipio.id = df_classe['id']
            municipio.codigo_ibge = df_classe['codigo_ibge']
            municipio.nome = df_classe['nome']
            municipio.nome_uf = df_classe['nome_uf']
            municipio.sigla_uf = df_classe['sigla_uf']
            municipio.ativo = df_classe['ativo']
            if exists:
                municipio.verified = True
            else:
                db.session.add(municipio)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_fornecedores_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_fornecedor in df.iterrows():
            fornecedor = Fornecedor.query.filter_by(id=df_fornecedor['id']).first()
            if fornecedor is None:
                exists = False
                fornecedor = Fornecedor()
            else:
                exists = True
            fornecedor.id = df_fornecedor['id']
            fornecedor.cnpj = df_fornecedor['cnpj']
            fornecedor.cpf = df_fornecedor['cpf']
            fornecedor.nome = df_fornecedor['nome']
            fornecedor.ativo = df_fornecedor['ativo']
            fornecedor.recadastrado = df_fornecedor['recadastrado']
            fornecedor.id_municipio = df_fornecedor['id_municipio']
            fornecedor.uf = df_fornecedor['uf']
            fornecedor.id_natureza_juridica = df_fornecedor['id_natureza_juridica']
            fornecedor.id_porte_empresa = df_fornecedor['id_porte_empresa']
            fornecedor.id_ramo_negocio = df_fornecedor['id_ramo_negocio']
            fornecedor.id_unidade_cadastradora = df_fornecedor['id_unidade_cadastradora']
            fornecedor.id_cnae = df_fornecedor['id_cnae']
            fornecedor.id_cnae2 = df_fornecedor['id_cnae2']
            fornecedor.habilitado_licitar = df_fornecedor['habilitado_licitar']
            if exists:
                fornecedor.verified = True
            else:
                db.session.add(fornecedor)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
    return None
