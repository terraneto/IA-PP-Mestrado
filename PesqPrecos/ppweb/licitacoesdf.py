from ppweb.ext.database import db
from ppweb.models import Uasg, Orgao, Licitacao
from ppweb.utils import logs


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
                orgao.verified = True
            else:
                db.session.add(orgao)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_licitacoes_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        print('tamanho do dataframe =' + str(len(df)))
        for index, df_licitacao in df.iterrows():
            print(index)
            licitacao = Licitacao.query.filter_by(uasg=df_licitacao['uasg'], modalidade=df_licitacao['modalidade'],
                                                  numero_aviso=df_licitacao['numero_aviso'],
                                                  numero_item_licitacao=df_licitacao['numero_item_licitacao']
                                                  ).first()
            if licitacao is None:
                exists = False
                licitacao = Licitacao()
            else:
                exists = True
            licitacao.uasg = df_licitacao['uasg']
            licitacao.modalidade = df_licitacao['modalidade']
            licitacao.numero_aviso = df_licitacao['numero_aviso']
            licitacao.identificador = df_licitacao['identificador']
            licitacao.numero_item_licitacao = df_licitacao['numero_item_licitacao']
            licitacao.tipo_pregao = df_licitacao['tipo_pregao']
            licitacao.situacao_aviso = df_licitacao['situacao_aviso']
            licitacao.objeto = df_licitacao['objeto']
            licitacao.codigo_do_item_no_catalogo = df_licitacao['codigo_do_item_no_catalogo']
            licitacao.informacoes_gerais = df_licitacao['informacoes_gerais']
            licitacao.numero_processo = df_licitacao['numero_processo']
            licitacao.tipo_recurso = df_licitacao['tipo_recurso']
            licitacao.numero_itens = df_licitacao['numero_itens']
            licitacao.nome_responsavel = df_licitacao['nome_responsavel']
            licitacao.funcao_responsavel = df_licitacao['funcao_responsavel']
            licitacao.data_entrega_edital = df_licitacao['data_entrega_edital']
            licitacao.endereco_entrega_edital = df_licitacao['endereco_entrega_edital']
            licitacao.data_abertura_proposta = df_licitacao['data_abertura_proposta']
            licitacao.data_entrega_proposta = df_licitacao['data_entrega_proposta']
            licitacao.data_publicacao = df_licitacao['data_publicacao']
            if exists:
                licitacao.verified = True
            else:
                db.session.add(licitacao)
            db.session.commit()
    except Exception as excecao:
        logs('licitacoes', df_licitacao['licitacao.identificador'])
        logs('licitacoes', str(df_licitacao['numero_item_licitacao']))
        print("Erro na gravação no banco " + str(excecao.__cause__))
