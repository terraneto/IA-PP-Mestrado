from ppweb.ext.database import db

from ppweb.models import Classe, Grupo, PDM, Material


def create_classes_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            classe = Classe()
            classe.codigo = df_classe['codigo']
            classe.descricao = df_classe['descricao']
            classe.codigo_grupo = df_classe['codigo_grupo']
            exists = db.session.query(db.exists().where(Classe.codigo == df_classe['codigo'])).scalar()
            if exists:
                classe.verified = True
            else:
                db.session.add(classe)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_grupos_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_grupo in df.iterrows():
            grupo = Grupo()
            grupo.codigo = df_grupo['codigo']
            grupo.descricao = df_grupo['descricao']
            exists = db.session.query(db.exists().where(Classe.codigo == df_grupo['codigo'])).scalar()
            if exists:
                grupo.verified = True
            else:
                db.session.add(grupo)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_pdms_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_pdm in df.iterrows():
            pdm = PDM()
            pdm.codigo = df_pdm['codigo']
            pdm.descricao = df_pdm['descricao']
            pdm.codigo_classe = df_pdm['codigo_classe']
            exists = db.session.query(db.exists().where(PDM.codigo == df_pdm['codigo'])).scalar()
            if exists:
                pdm.verified = True
            else:
                db.session.add(pdm)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_materiais_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_material in df.iterrows():
            material = Material()
            material.codigo = df_material['codigo']
            material.descricao = df_material['descricao']
            material.id_grupo = df_material['id_grupo']
            material.id_classe = df_material['id_classe']
            material.id_pdm = df_material['id_pdm']
            material.status = df_material['status']
            material.sustentavel = df_material['sustentavel']
            exists = db.session.query(db.exists().where(Material.codigo == df_material['codigo'])).scalar()
            if exists:
                material.verified = True
            else:
                db.session.add(material)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
