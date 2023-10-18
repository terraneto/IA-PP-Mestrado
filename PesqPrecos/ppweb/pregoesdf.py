from ppweb.ext.database import db
from ppweb.models import Itempregao, Pregao


def create_pregoes_from_dataframe(df):
    try:
        for index, dfpregao in df.iterrows():
            vnumero = int(dfpregao['numero'])
            pregao = Pregao.query.filter_by(numero=vnumero).first()
            if pregao is None:
                exists = False
                pregao = Pregao()
            else:
                exists = True
            pregao.numero = int(dfpregao['numero'])
            pregao.co_portaria = dfpregao['co_portaria']
            pregao.dtPortaria = dfpregao['dtPortaria']
            pregao.co_processo = dfpregao['co_processo']
            pregao.ds_tipo_pregao = dfpregao['ds_tipo_pregao']
            pregao.ds_tipo_pregao_compra = dfpregao['ds_tipo_pregao_compra']
            pregao.tx_objeto = dfpregao['tx_objeto']
            pregao.valorHomologadoTotal = float(dfpregao['valorHomologadoTotal'])
            pregao.valorEstimadoTotal = float(dfpregao['valorEstimadoTotal'])
            pregao.co_uasg = int(dfpregao['co_uasg'])
            pregao.ds_situacao_pregao = dfpregao['ds_situacao_pregao']
            pregao.dtDataEdital = dfpregao['dtDataEdital']
            pregao.dtInicioProposta = dfpregao['dtInicioProposta']
            pregao.dtFimProposta = dfpregao['dtFimProposta']
            if exists:
                pregao.verified = True
            else:
                db.session.add(pregao)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        db.session.rollback()
        print(excecao.args)


def create_itenspregoes_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_itens in df.iterrows():
            vid = int(df_itens['id'])
            itempregao = Itempregao.query.filter_by(id=vid).first()
            if itempregao is None:
                exists = False
                itempregao = Itempregao()
            else:
                exists = True
            itempregao.id = vid
            itempregao.id_pregao = df_itens['id_pregao']
            itempregao.num_item = df_itens['num_item']
            itempregao.descricao_item = df_itens['descricao_item']
            itempregao.quantidade_item = df_itens['quantidade_item']
            itempregao.valor_estimado_item = df_itens['valor_estimado_item']
            itempregao.descricao_detalhada_item = df_itens['descricao_detalhada_item']
            itempregao.tratamento_diferenciado = df_itens['tratamento_diferenciado']
            itempregao.decreto_7174 = df_itens['decreto_7174']
            itempregao.margem_preferencial = df_itens['margem_preferencial']
            itempregao.unidade_fornecimento = df_itens['unidade_fornecimento']
            itempregao.situacao_item = df_itens['situacao_item']
            itempregao.fornecedor_vencedor = df_itens['fornecedor_vencedor']
            itempregao.menor_lance = df_itens['menor_lance']
            itempregao.valorHomologadoItem = df_itens['valorHomologadoItem']
            itempregao.valor_negociado = df_itens['valor_negociado']
            if exists:
                itempregao.verified = True
            else:
                db.session.add(itempregao)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        db.session.rollback()
        print(excecao.args)
