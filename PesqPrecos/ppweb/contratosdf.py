from ppweb.ext.database import db

from ppweb.models import ComprasContratos
import datetime as dt


def create_contratos_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            print(index)
            exists = db.session.query(db.exists().where(ComprasContratos.id == df_classe['id'])).scalar()
            if exists:
                contrato = ComprasContratos.query.filter_by(id=df_classe['id']).first()
            else:
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
            contrato.codigo_tipo = df_classe['codigo_tipo']
            contrato.tipo = df_classe['tipo']
            contrato.categoria = df_classe['categoria']
            contrato.processo = df_classe['processo']
            contrato.objeto = df_classe['objeto']
            contrato.fundamento_legal = df_classe['fundamento_legal']
            contrato.data_assinatura = df_classe['data_assinatura']
            contrato.data_publicacao = df_classe['data_publicacao']
            contrato.vigencia_inicio = df_classe['vigencia_inicio']
            contrato.vigencia_fim = df_classe['vigencia_fim']
            contrato.valor_inicial = df_classe['valor_inicial']
            contrato.valor_global = df_classe['valor_global']
            contrato.num_parcelas = df_classe['num_parcelas']
            contrato.valor_parcela = df_classe['valor_parcela']
            contrato.valor_acumulado = df_classe['valor_acumulado']
            contrato.fornecedor_tipo = df_classe['fornecedor_tipo']
            contrato.fornecedor_cnpj_cpf_idgener = df_classe['fornecedor_cnpj_cpf_idgener']
            contrato.fornecedor_nome = df_classe['fornecedor_nome']
            contrato.codigo_compra = df_classe['codigo_compra']
            contrato.modalidade_codigo = df_classe['modalidade_codigo']
            contrato.modalidade = df_classe['modalidade']
            contrato.unidade_compra = df_classe['unidade_compra']
            contrato.licitacao_numero = df_classe['licitacao_numero']
            contrato.informacao_complementar = df_classe['informacao_complementar']
            if exists:
                contrato.verified = True
            else:
                db.session.add(contrato)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
