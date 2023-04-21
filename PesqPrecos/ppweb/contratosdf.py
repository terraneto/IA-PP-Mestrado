import json
import os
import calendar

from ppweb.ext.database import db

from ppweb.models import ComprasContratos, Itenscontratos
from ppweb.utils import logs, request_json


def baixa_json_contrato_anual(vano):
    ptipo = "contratos"
    inicio = vano + '-01-01'
    fim = vano + '-12-31'
    pag = 0
    numpags = 79
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    while pag < numpags:
        valpag = 500 * pag
        url = 'http://compras.dados.gov.br/comprasContratos/v1/contratos.json?' + \
              'data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim + '&offset=' + str(valpag)
        arquivo = "contratos" + vano + '-' + str(valpag).zfill(4) + '.json'
        patharquivo = './static/json/contratos/' + arquivo
        print(url)
        baixou = request_json(url, "contratos", arquivo)
        if baixou:
            with open(patharquivo) as jsonfile:
                data_json = json.load(jsonfile)
                num = data_json["count"]
                totalpag = num // 500
                if num % 500 > 0:
                    totalpag = totalpag + 1
                numpags = totalpag
        pag += 1
        print('baixada ' + str(pag) + '/' + str(numpags))
    return True


def baixa_json_contrato_mes(vano, vmes):
    ptipo = "contratos"
    mes = int(vmes)
    ano = int(vano)
    mesinic = mes - 1
    mesfim = mes + 1
    anoinic = ano
    anofim = ano
    if mesinic == 0:
        anoinic = anoinic - 1
        mesinic = 12
    if mesfim > 12:
        anofim = anofim + 1
        mesfim = 1
    inicio = str(anoinic).zfill(4) + '-' + str(mesinic).zfill(2) + '-' + \
             str(calendar.monthrange(anoinic, mesinic)[1]).zfill(2)
    fim = str(anofim).zfill(4) + '-' + str(mesfim).zfill(2) + '-01'
    pag = 0
    numpags = 1
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    while pag < numpags:
        valpag = 500 * pag
        url = 'http://compras.dados.gov.br/comprasContratos/v1/contratos.json?' + \
              'data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim + '&offset=' + str(valpag)
        arquivo = "contratos" + vano + '-' + vmes + '-' + str(valpag).zfill(4) + '.json'
        patharquivo = './static/json/contratos/' + arquivo
        print(url)
        baixou = request_json(url, "contratos", arquivo)
        if baixou:
            with open(patharquivo) as jsonfile:
                data_json = json.load(jsonfile)
                num = data_json["count"]
                totalpag = num // 500
                if num % 500 > 0:
                    totalpag = totalpag + 1
                numpags = totalpag
        pag += 1
        print('baixada ' + str(pag) + '/' + str(numpags))
    return True


def baixa_json_contrato_mensal(vano):
    ano = int(vano)
    modulo = "comprasContratos"
    ptipo = "contratos"
    for mes in range(1, 13):
        udia = calendar.monthrange(ano, mes)[1]
        smes = str(ano).zfill(4) + '-' + str(mes).zfill(2)
        diainicio = 1
        diafim = udia
        inicio = smes + '-' + str(diainicio).zfill(2)
        fim = smes + '-' + str(diafim).zfill(2)
        pag = 0
        numpags = 1
        logs(ptipo,
             'Iniciou download mês ' + str(mes) + ' número páginas=' + str(numpags))
        if not os.path.exists('./static/json/' + ptipo):
            os.mkdir('./static/json/' + ptipo)
        while pag < numpags:
            valpag = 500 * pag
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?' + \
                  'data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim + '&offset=' + str(valpag)
            arquivo = ptipo + smes + '-' + str(valpag).zfill(4) + '.json'
            patharquivo = './static/json/' + ptipo + '/' + arquivo
            oldarquivo = './static/json/' + ptipo + '/old' + arquivo
            if os.path.exists(patharquivo) and pag > 0:
                pag += 1
                logs(ptipo, 'Pulou pagina=' + str(pag))
                continue
            print(url)
            if pag == 0:
                if os.path.exists(patharquivo):
                    if not os.path.exists(oldarquivo):
                        os.rename(patharquivo, oldarquivo)
            baixou = request_json(url, ptipo, arquivo)
            if baixou or pag == 0:
                if not baixou:
                    print(oldarquivo)
                    if not os.path.exists(patharquivo):
                        if os.path.exists(oldarquivo):
                            os.rename(oldarquivo, patharquivo)
                        else:
                            continue
                with open(patharquivo) as jsonfile:
                    data_json = json.load(jsonfile)
                    num = data_json["count"]
                    totalpag = num // 500
                    if num % 500 > 0:
                        totalpag = totalpag + 1
                    numpags = totalpag
            pag += 1
            print('baixada ' + str(pag) + '/' + str(numpags))
            logs(ptipo, 'Terminou paginas=' + str(pag))
            logs(ptipo, 'número paginas=' + str(numpags))
            if os.path.exists(oldarquivo):
                os.remove(oldarquivo)
    return True


def baixa_json_itenscontrato():
    i = 0
    identificadores = db.session.query(ComprasContratos.id).distinct().all()
    for contrato in identificadores:
        i = i + 1
        print('baixando itens - ' + str(i))
        if not os.path.exists('./static/json/itenscontrato'):
            os.mkdir('./static/json/itenscontrato')
        url = 'http://compras.dados.gov.br/comprasContratos/id/contrato/' + str(contrato.id) \
              + '/itens_compras_contratos.json'
        print(url)
        arquivo = str(contrato.id) + '.json'
        patharquivo = './static/json/itenscontrato/' + arquivo
        if not os.path.exists(patharquivo):
            request_json(url, 'itenscontrato', arquivo)
    return True


def create_contratos_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
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


def create_itenscontratos_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        for index, df_classe in df.iterrows():
            exists = db.session.query(db.exists().where(Itenscontratos.id == df_classe['id'])).scalar()
            if exists:
                contrato = Itenscontratos.query.filter_by(id=df_classe['id']).first()
            else:
                contrato = Itenscontratos()
            contrato.id = df_classe['id']
            contrato.contrato_id = df_classe['contrato_id']
            contrato.tipo_id = df_classe['tipo_id']
            contrato.grupo_id = df_classe['grupo_id']
            contrato.catmatser_item_id = df_classe['catmatser_item_id']
            contrato.descricao_complementar = df_classe['descricao_complementar']
            contrato.quantidade = df_classe['quantidade']
            contrato.valor_unitario = df_classe['valor_unitario']
            contrato.valor_total = df_classe['valor_total']
            if exists:
                contrato.verified = True
            else:
                db.session.add(contrato)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
