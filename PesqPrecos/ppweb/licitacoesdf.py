from ppweb.ext.database import db

from ppweb.models import Uasg, Orgao


def create_uasg_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        if 'total_fornecedores_recadastrados' in df.columns:
            del df['total_fornecedores_recadastrados']
        for index, df_uasg in df.iterrows():
            uasg = Uasg()
            uasg.id = df_uasg['id']
            uasg.cnpj = df_uasg['cnpj']
            uasg.nome = df_uasg['nome']
            uasg.cep = df_uasg['cep']
            uasg.ativo = df_uasg['ativo']
            uasg.id_orgao = df_uasg['id_orgao']
            uasg.id_municipio = df_uasg['id_municipio']
            uasg.id_orgao_superior = df_uasg['id_orgao_superior']
            uasg.total_fornecedores_cadastrados = df_uasg['total_fornecedores_cadastrados']
            uasg.unidade_cadastradora = df_uasg['unidade_cadastradora']
            exists = db.session.query(db.exists().where(Uasg.id == df_uasg['id'])).scalar()
            if exists:
                uasg.verified = True
            else:
                db.session.add(uasg)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_orgaos_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        if 'codigo_siorg' in df.columns:
            del df['codigo_siorg']
        for index, df_orgao in df.iterrows():
            orgao = Orgao()
            orgao.codigo = df_orgao['codigo']
            orgao.nome = df_orgao['nome']
            orgao.codigo_tipo_adm = df_orgao['codigo_tipo_adm']
            if df_orgao['codigo_tipo_esfera'] is None:
                orgao.codigo_tipo_esfera = ''
            else:
                orgao.codigo_tipo_esfera = df_orgao['codigo_tipo_esfera']
            orgao.codigo_tipo_poder = df_orgao['codigo_tipo_poder']
            orgao.ativo = df_orgao['ativo']
            exists = db.session.query(db.exists().where(Orgao.codigo == df_orgao['codigo'])).scalar()
            if exists:
                Orgao.verified = True
            else:
                db.session.add(orgao)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
