from ppweb.ext.database import db

from ppweb.models import AmbitoOcorrencia, CNAE, Municipio


def create_ambitos_ocorrencia_from_dataframe(df):
    print(df)
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            ambitoocorrencia = AmbitoOcorrencia()
            ambitoocorrencia.id = df_classe['id']
            ambitoocorrencia.descricao = df_classe['descricao']
            exists = db.session.query(db.exists().where(AmbitoOcorrencia.id == df_classe['id'])).scalar()
            if exists:
                ambitoocorrencia.verified = True
            else:
                db.session.add(ambitoocorrencia)
            print(ambitoocorrencia)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_cnaes_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            cnae = CNAE()
            cnae.id = df_classe['id']
            cnae.descricao = df_classe['descricao']
            cnae.codigo_longo = df_classe['codigo_longo']
            exists = db.session.query(db.exists().where(CNAE.id == df_classe['id'])).scalar()
            if exists:
                cnae.verified = True
            else:
                db.session.add(cnae)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_municipios_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            municipio = Municipio()
            municipio.id = df_classe['id']
            municipio.codigo_ibge = df_classe['codigo_ibge']
            municipio.nome = df_classe['nome']
            municipio.nome_uf = df_classe['nome_uf']
            municipio.sigla_uf = df_classe['sigla_uf']
            municipio.ativo = df_classe['ativo']
            exists = db.session.query(db.exists().where(Municipio.id == df_classe['id'])).scalar()
            if exists:
                municipio.verified = True
            else:
                db.session.add(municipio)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
