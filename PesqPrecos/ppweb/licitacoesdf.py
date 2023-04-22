import calendar
import json
import os
from datetime import date, timedelta

import pandas as pd2

from ppweb.ext.database import db
from ppweb.models import Uasg, Orgao, Licitacao, Itenslicitacao, Classe, Material, Itensprecospraticados
from ppweb.utils import logs, request_json


def baixa_uasg_mes(uasg, vano, vmes):
    inicio = vano + '-' + vmes + '-01'
    udia = calendar.monthrange(int(vano), int(vmes))[1]
    fim = vano + '-' + vmes + '-' + str(udia).zfill(2)
    logs('licitacoes', 'Iniciou download do mes ' + vano + '-' + vmes + ' - ' + uasg)
    if not os.path.exists('./static/json/licitacoes/' + vano + '/mensal'):
        os.mkdir('./static/json/licitacoes/' + vano + '/mensal')
    url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?uasg=' + uasg + \
          '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
    logs('licitacoes', url)
    arquivo = 'licitacoes-' + str(int(uasg)).zfill(6) + '-' + vano + '-' + vmes + '.json'
    patharquivo = './static/json/licitacoes/' + vano + '/mensal' + '/' + arquivo
    baixou = request_json(url, 'licitacoes/' + vano + '/mensal', arquivo)
    if baixou:
        with open(patharquivo) as jsonfile:
            mdata_json = json.load(jsonfile)
            mnum = mdata_json["count"]
        if mnum > 0:
            if ((mnum // 500) == 1) and (mnum % 500 == 0):
                logs('baixa_uasg_mes', 'excedeu o número de licitacoes no mes')
                baixa_uasg_diario(uasg, vano, vmes)
    return True


def baixa_json_licitacao_uasg_trimestral():
    uasgs = Uasg.query.filter_by(ativo=True).all()
    numu = len(uasgs)
    data_atual = date.today()
    data_inicial = data_atual - timedelta(days=90)
    for parte in range(1, 4):
        u = 0
        vano = str(data_inicial.year).zfill(4)
        vmes = str(data_inicial.month).zfill(2)
        for uasg in uasgs:
            u = u + 1
            print('iniciando uasg ' + str(u) + ' de ' + str(numu))
            vid = str(uasg.id)
            baixa_uasg_mes(vid, vano, vmes)
        data_inicial = data_inicial + timedelta(days=30)
    return True


def baixa_json_licitacao_uasg_mensal(vano, vmes):
    query = db.session.query(Licitacao.uasg.distinct().label("uasg"))
    uasgs = [row.uasg for row in query.all()]
    numu = len(uasgs)
    udia = calendar.monthrange(int(vano), int(vmes))[1]
    u = 0
    for uasg in uasgs:
        u = u + 1
        vid = uasg
        print('baixa Json licitacoes ' + str(u) + '/' + str(numu))
        inicio = vano + '-' + vmes + '-01'
        fim = vano + '-' + vmes + '-' + str(udia).zfill(2)
        logs('licitacoes', 'Iniciou download mensal ' + vano + '-' + vmes + ' - ' + str(vid))
        if not os.path.exists('./static/json/' + 'licitacoes'):
            os.mkdir('./static/json/' + 'licitacoes')
        url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?uasg=' + str(vid) + \
              '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
        logs('licitacoes', url)
        arquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vano + '.json'
        patharquivo = './static/json/licitacoes' + '/' + arquivo
        if not os.path.exists(patharquivo):
            baixou = request_json(url, 'licitacoes', arquivo)
            if baixou:
                with open(patharquivo) as jsonfile:
                    mdata_json = json.load(jsonfile)
                    mnum = mdata_json["count"]
                if mnum > 0:
                    if ((mnum // 500) == 1) and (mnum % 500 == 0):
                        os.remove(patharquivo)
                        logs('baixa_json_licitacao_uasg_mensal', 'excedeu o numero de licitacoes no mes')
                        baixa_uasg_diario(uasg, vano, vmes)
    return True


def baixa_uasg_mensal(uasg, mvano):
    vid = uasg
    mano = int(mvano)
    print('baixa Json licitacoes mensal')
    for mmes in range(1, 13):
        mudia = calendar.monthrange(mano, mmes)[1]
        msmes = str(mano).zfill(4) + '-' + str(mmes).zfill(2)
        mdiainicio = 1
        mdiafim = mudia
        minicio = msmes + '-' + str(mdiainicio).zfill(2)
        mfim = msmes + '-' + str(mdiafim).zfill(2)
        logs('licitacoes', 'Iniciou download mês ' + str(mmes) + ' - ' + str(vid))
        if not os.path.exists('./static/json/' + 'licitacoes'):
            os.mkdir('./static/json/' + 'licitacoes')
        url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
              '&data_publicacao_min=' + minicio + '&data_publicacao_max=' + mfim
        logs('licitacoes', url)
        marquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + msmes + '.json'
        mpatharquivom = './static/json/' + 'licitacoes' + '/' + marquivo
        mbaixoum = False
        if not os.path.exists(mpatharquivom):
            mbaixoum = request_json(url, 'licitacoes', marquivo)
        if mbaixoum:
            with open(mpatharquivom) as jsonfile:
                mdata_json = json.load(jsonfile)
                mnum = mdata_json["count"]
            if mnum > 0:
                mtotalpag = mnum // 500
                if ((mtotalpag == 1) and (mnum % 500 == 0)) or (mnum == 0):
                    logs('baixa_uasg_mensal',
                         'arquivo com excesso de licitacoes no mes de ' + str(mmes) + '- num= ' + str(mnum))
                    baixa_uasg_diario(uasg, mvano, str(mmes))
    return True


def baixa_uasg_diario(uasg, dvano, dvmes):
    vid = uasg
    dano = int(dvano)
    dmes = int(dvmes)
    dudia = calendar.monthrange(dano, dmes)[1]
    print('baixa Json licitacoes diárias')
    for ddia in range(1, dudia + 1):
        dsmes = str(dano).zfill(4) + '-' + str(dmes).zfill(2)
        vdia = dsmes + '-' + str(ddia).zfill(2)
        if not os.path.exists('./static/json/licitacoes/'+dvano+'/diario'):
            os.mkdir('./static/json/licitacoes/'+dvano+'/diario')
        url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
              '&data_publicacao=' + vdia
        logs('licitacoes', url)
        darquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + dsmes + '-' + str(ddia).zfill(2) + '.json'
        request_json(url, 'licitacoes/'+dvano+'/diario', darquivo)
    return True


def baixa_uasg_dia_classe(uasg, dia):
    vid = uasg
    vdia = dia
    classes = Classe.query.all()
    c = 0
    print('baixa Json licitacoes diárias')
    for classe in classes:
        c = c + 1
        logs('baixa_uasg_dia_classe',
             'Classe ' + str(classe.codigo) + ' de um total de ' + str(c) + '/' + str(len(classes)))
        idclasse = str(classe.codigo).zfill(4)
        if not os.path.exists('./static/json/' + 'licitacoes'):
            os.mkdir('./static/json/' + 'licitacoes')
        url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
              '&data_publicacao=' + vdia + '&item_material_classificacao=' + idclasse
        logs('licitacoes', url)
        dcarquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vdia + '-' + idclasse + '.json'
        dcpatharquivod = './static/json/' + 'licitacoes' + '/' + dcarquivo
        dcbaixoud = False
        if not os.path.exists(dcpatharquivod):
            dcbaixoud = request_json(url, 'licitacoes', dcarquivo)
        if dcbaixoud:
            with open(dcpatharquivod) as jsonfile:
                dcdata_json = json.load(jsonfile)
                dcnum = dcdata_json["count"]
            if ((dcnum // 500) == 1) and (dcnum % 500 == 0):
                os.remove(dcpatharquivod)
                logs('baixa_uasg_dia_classe', 'excedeu o numero de licitacoes na classe ' + idclasse +
                     'número de licitações=' + str(dcnum))
                baixa_uasg_dia_material(uasg, vdia, idclasse)
    return True


def baixa_uasg_dia_material(uasg, dia, classe):
    vid = uasg
    vdia = dia
    vclasse = classe
    print('Pesquisando Materiais')
    materiais = Material.query.filter_by(id_classe=int(vclasse), status=1).all()
    logs('materiais na classe ' + vclasse + ' ', str(len(materiais)))
    print(str(len(materiais)))
    print('baixa Json licitacoes diárias')
    for material in materiais:
        if not os.path.exists('./static/json/' + 'licitacoes'):
            os.mkdir('./static/json/' + 'licitacoes')
        url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
              '&data_publicacao=' + vdia + '&item_material=' + str(material.codigo)
        logs('licitacoes', url)
        dmarquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vdia + '-' + vclasse + '-' + str(
            material.codigo) + '.json'
        dmpatharquivod = './static/json/' + 'licitacoes' + '/' + dmarquivo
        dmbaixoud = False
        if not os.path.exists(dmpatharquivod):
            dmbaixoud = request_json(url, 'licitacoes', dmarquivo)
        if dmbaixoud:
            with open(dmpatharquivod) as jsonfile:
                dmdata_json = json.load(jsonfile)
                dmnum = dmdata_json["count"]
            if dmnum > 0:
                dmtotalpag = dmnum // 500
                if (dmtotalpag == 1) and (dmnum % 500 == 0):
                    logs('licitacoes', 'licitacoes do material em excesso ' + dmarquivo)
    return True


def baixa_json_uasg_licitacoes_mensal(vano, vmes):
    ano = int(vano)
    mes = int(vmes)
    query = db.session.query(Licitacao.uasg.distinct().label("uasg"))
    uasgs = [row.uasg for row in query.all()]
    numu = len(uasgs)
    u = 0
    for uasg in uasgs:
        u = u + 1
        vid = uasg
        print('baixa Json licitacoes mensal ' + vmes + '/' + vano + 'uasg ' + str(u) + '/' + str(numu))
        inicio = vano + '-' + vmes + '-01'
        if vmes == '12':
            vanofim = str(ano + 1).zfill(4)
            fim = vanofim + '-01-01'
        else:
            vmesfim = str(mes + 1).zfill(2)
            fim = vano + '-' + vmesfim + '-01'
        if not os.path.exists('./static/json/licitacoes'):
            os.mkdir('./static/json/licitacoes')
        url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?uasg=' + str(vid) + \
              '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
        arquivo = 'licitacoes' + str(vid).zfill(6) + '-' + vano + '-' + vmes + '.json'
        patharquivo = './static/json/licitacoes/' + arquivo
        baixou = request_json(url, 'licitacoes', arquivo)
        if baixou:
            with open(patharquivo) as jsonfile:
                data_json = json.load(jsonfile)
                num = data_json["count"]
                print('numero de licitacoes = ' + str(num))
                embedded = data_json["_embedded"]
                if num > 0:
                    tb = embedded["licitacoes"]
                    df = pd2.DataFrame.from_dict(tb, orient='columns')
                    print('tamanho do dataframe =' + str(len(df)))
                    i = 0
                    for index, df_licitacao in df.iterrows():
                        licitacao = df_licitacao['identificador']
                        i = i + 1
                        print('baixando itens da licitacao - ' + str(i))
                        if not os.path.exists('./static/json/itenslicitacao'):
                            os.mkdir('./static/json/itenslicitacao')
                            url = 'http://compras.dados.gov.br/licitacoes/id/licitacao/' + licitacao.identificador + \
                                  '/itens.json '
                            print(url)
                            arquivoi = licitacao.identificador + '.json'
                            request_json(url, 'itenslicitacao', arquivoi)
    return True


def baixa_json_itenslicitacao():
    i = 0
    identificadores = db.session.query(Licitacao.identificador).distinct().all()
    for licitacao in identificadores:
        i = i + 1
        logs('itenslicitacao', 'baixando itens - ' + str(i))
        if not os.path.exists('./static/json/itenslicitacao'):
            os.mkdir('./static/json/itenslicitacao')
        url = 'http://compras.dados.gov.br/licitacoes/id/licitacao/' + licitacao.identificador + '/itens.json'
        logs('itenslicitacao', url)
        arquivo = licitacao.identificador + '.json'
        patharquivo = './static/json/itenslicitacao/' + arquivo
        if not os.path.exists(patharquivo):
            request_json(url, 'itenslicitacao', arquivo)
    return True


def baixa_json_itensprecospraticados():
    i = 0
    identificadores = db.session.query(Licitacao.identificador).distinct().all()
    for licitacao in identificadores:
        i = i + 1
        logs('itensprecospraticados', 'baixando itens - ' + str(i))
        if not os.path.exists('./static/json/itensprecospraticados'):
            os.mkdir('./static/json/itensprecospraticados')
        url = 'http://compras.dados.gov.br/licitacoes/id/preco_praticado/' + licitacao.identificador + '/itens.json'
        logs('itensprecospraticados', url)
        arquivo = licitacao.identificador + '.json'
        patharquivo = './static/json/itensprecospraticados/' + arquivo
        if not os.path.exists(patharquivo):
            request_json(url, 'itensprecospraticados', arquivo)
    return True


def create_uasg_from_dataframe(df):
    try:
        if '_links' in df.columns:
            del df['_links']
        #if 'total_fornecedores_recadastrados' in df.columns:
        #    del df['total_fornecedores_recadastrados']

        for index, df_uasg in df.iterrows():
            uasg = Uasg.query.filter_by(id=df_uasg['id']).first()
            if uasg is None:
                exists = False
                uasg = Uasg()
            else:
                exists = True
            uasg.id = df_uasg['id']
            uasg.cnpj = df_uasg['cnpj']
            uasg.nome = df_uasg['nome']
            uasg.cep = df_uasg['cep']
            uasg.ativo = df_uasg['ativo']
            uasg.id_orgao = df_uasg['id_orgao']
            uasg.id_municipio = df_uasg['id_municipio']
            uasg.id_orgao_superior = df_uasg['id_orgao_superior']
            uasg.total_fornecedores_cadastrados = df_uasg['total_fornecedores_cadastrados']
            uasg.total_fornecedores_recadastrados = df_uasg['total_fornecedores_recadastrados']
            uasg.unidade_cadastradora = df_uasg['unidade_cadastradora']
            if exists:
                uasg.verified = True
            else:
                db.session.add(uasg)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        print(excecao.args)


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
        for index, df_licitacao in df.iterrows():
            licitacao = Licitacao.query.filter_by(uasg=df_licitacao['uasg'], modalidade=df_licitacao['modalidade'],
                                                  numero_aviso=df_licitacao['numero_aviso']
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
            licitacao.tipo_pregao = df_licitacao['tipo_pregao']
            licitacao.situacao_aviso = df_licitacao['situacao_aviso']
            licitacao.objeto = df_licitacao['objeto']
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
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_itenslicitacao_from_dataframe(df):
    try:
        for index, df_licitacao in df.iterrows():
            itemlicitacao = Itenslicitacao.query.filter_by(uasg=df_licitacao['uasg'],
                                                           modalidade=df_licitacao['modalidade'],
                                                           numero_aviso=df_licitacao['numero_aviso'],
                                                           numero_item_licitacao=df_licitacao['numero_item_licitacao']
                                                           ).first()
            if itemlicitacao is None:
                exists = False
                itemlicitacao = Itenslicitacao()
            else:
                exists = True
            itemlicitacao.uasg = df_licitacao['uasg']
            itemlicitacao.modalidade = df_licitacao['modalidade']
            itemlicitacao.numero_aviso = df_licitacao['numero_aviso']
            itemlicitacao.numero_licitacao = df_licitacao['numero_licitacao']
            itemlicitacao.numero_item_licitacao = df_licitacao['numero_item_licitacao']
            itemlicitacao.codigo_item_servico = df_licitacao['codigo_item_servico']
            itemlicitacao.codigo_item_material = df_licitacao['codigo_item_material']
            itemlicitacao.descricao_item = df_licitacao['descricao_item']
            itemlicitacao.sustentavel = df_licitacao['sustentavel']
            itemlicitacao.quantidade = df_licitacao['quantidade']
            itemlicitacao.unidade = df_licitacao['unidade']
            itemlicitacao.cnpj_fornecedor = df_licitacao['cnpj_fornecedor']
            itemlicitacao.cpfVencedor = df_licitacao['cpfVencedor']
            itemlicitacao.beneficio = df_licitacao['beneficio']
            itemlicitacao.valor_estimado = df_licitacao['valor_estimado']
            itemlicitacao.decreto_7174 = df_licitacao['decreto_7174']
            itemlicitacao.criterio_julgamento = df_licitacao['criterio_julgamento']
            if exists:
                itemlicitacao.verified = True
            else:
                db.session.add(itemlicitacao)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def create_itensprecospraticados_from_dataframe(df):
    try:
        for index, df_licitacao in df.iterrows():
            itemprecopraticado = Itensprecospraticados.query.filter_by(uasg=df_licitacao['uasg'],
                                                                       modalidade=df_licitacao['modalidade'],
                                                                       numero_aviso=df_licitacao['numero_aviso'],
                                                                       numero_item_licitacao=df_licitacao[
                                                                           'numero_item_licitacao']
                                                                       ).first()
            if itemprecopraticado is None:
                exists = False
                itemprecopraticado = Itensprecospraticados()
            else:
                exists = True
            itemprecopraticado.uasg = df_licitacao['uasg']
            itemprecopraticado.modalidade = df_licitacao['modalidade']
            itemprecopraticado.numero_aviso = df_licitacao['numero_aviso']
            itemprecopraticado.numero_item_licitacao = df_licitacao['numero_item_licitacao']
            itemprecopraticado.codigo_item_servico = df_licitacao['codigo_item_servico']
            itemprecopraticado.codigo_item_material = df_licitacao['codigo_item_material']
            itemprecopraticado.cnpj_fornecedor = df_licitacao['cnpj_fornecedor']
            itemprecopraticado.marca = df_licitacao['marca']
            itemprecopraticado.unidade = df_licitacao['unidade']
            itemprecopraticado.quantidade = df_licitacao['quantidade']
            itemprecopraticado.valor_unitario = df_licitacao['valor_unitario']
            itemprecopraticado.valor_total = df_licitacao['valor_total']
            itemprecopraticado.beneficio = df_licitacao['beneficio']
            itemprecopraticado.id_licitacao = df_licitacao['id_licitacao']
            if exists:
                itemprecopraticado.verified = True
            else:
                db.session.add(itemprecopraticado)
            db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def baixa_uasg_diario_material_geral(ano):
    path = './static/json/licitacoes/'+ano+'/classes'
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Verificando arquivos de classes e dividindo em material ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
        except:
            continue
        numero = data_json["count"]
        if numero != 500:
            continue
        uasg = nomearq[11:17]
        vid = int(uasg)
        vdia = nomearq[18:28]
        vclasse = nomearq[29:33]
        materiais = Material.query.filter_by(id_classe=int(vclasse), status=1).all()
        logs('materiais', str(len(materiais)))
        totalm = str(len(materiais))
        m = 0
        for material in materiais:
            m = m + 1
            if not os.path.exists('./static/json/licitacoes/'+ano + '/material'):
                os.mkdir('./static/json/licitacoes/'+ano + '/material')
            url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
                  '&data_publicacao=' + vdia + '&item_material=' + str(material.codigo)
            dmarquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vdia + '-' + vclasse + '-' + str(
                material.codigo) + '.json'
            dmpatharquivod = './static/json/licitacoes/'+ano + '/material' + '/' + dmarquivo
            if not os.path.exists(dmpatharquivod):
                print(str(i) + '/' + str(numdir) + ' - ' + url + ' - ' + str(m) + ' de ' + totalm)
                request_json(url, 'licitacoes/'+ano + '/material', dmarquivo)
    return True


def baixa_uasg_diario_classe_geral(ano, recursivo):
    path = './static/json/licitacoes/'+ano+'/diario'
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Verificando arquivos diarios e dividindo em classes ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
        except:
            continue
        numero = data_json["count"]
        if numero != 500:
            continue
        uasg = nomearq[11:17]
        vid = int(uasg)
        vdia = nomearq[18:28]
        classes = Classe.query.all()
        nclasses = len(classes)
        c = 0
        for classe in classes:
            c = c + 1
            logs('baixa_uasg_dia_classe',
                 'Classe ' + str(classe.codigo) + ' de um total de ' + str(c) + '/' + str(len(classes)))
            idclasse = str(classe.codigo).zfill(4)
            if not os.path.exists('./static/json/licitacoes/'+ano + '/classes'):
                os.mkdir('./static/json/licitacoes/'+ano + '/classes')
            url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
                  '&data_publicacao=' + vdia + '&item_material_classificacao=' + idclasse
            logs('licitacoes', url)
            dcarquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vdia + '-' + idclasse + '.json'
            dcpatharquivod = './static/json/licitacoes/'+ano + '/classes/' + dcarquivo
            if not os.path.exists(dcpatharquivod):
                print('diario ' + str(i) + '/' + str(numdir) + ' Classe ' + str(c) + ' de ' + str(nclasses) + ' ' + url)
                request_json(url, 'licitacoes/'+ano + '/classes', dcarquivo)
    if recursivo == 'S':
        baixa_uasg_diario_material_geral(ano)
    return True


def baixa_uasg_mensal_diario_geral(ano, recursivo):
    path = './static/json/licitacoes/'+ano+'/mensal'
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Verificando arquivos mensais e dividindo em dias ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
        except:
            continue
        numero = data_json["count"]
        if numero != 500:
            continue
        uasg = nomearq[11:17]
        vid = int(uasg)
        vsano = nomearq[18:22]
        dano = int(vsano)
        vsmes = nomearq[23:25]
        dmes = int(vsmes)
        dudia = calendar.monthrange(dano, dmes)[1]
        for ddia in range(1, dudia + 1):
            dsmes = str(dano).zfill(4) + '-' + str(dmes).zfill(2)
            vdia = dsmes + '-' + str(ddia).zfill(2)
            if not os.path.exists('./static/json/licitacoes/'+ano+'/diario'):
                os.mkdir('./static/json/licitacoes/'+ano+'/diario')
            url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
                  '&data_publicacao=' + vdia
            logs('licitacoes', url)
            darquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + dsmes + '-' + str(ddia).zfill(2) + '.json'
            dpatharquivod = './static/json/licitacoes/'+ano+'/diario' + '/' + darquivo
            if not os.path.exists(dpatharquivod):
                print('Mês ' + str(i) + '/' + str(numdir) + ' dia ' + str(ddia) + ' de ' + str(dudia) + ' ' + url)
                request_json(url, 'licitacoes/'+ano+'/diario', darquivo)
    if recursivo == 'S':
        baixa_uasg_diario_classe_geral(ano)
    return True


def baixa_uasg_mensal_geral(ano, recursivo):
    path = './static/json/licitacoes/'+ano
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Verificando arquivos anuais e dividindo em mes ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
        except:
            continue
        numero = data_json["count"]
        if numero != 500:
            continue
        uasg = nomearq[11:17]
        vid = int(uasg)
        vsano = nomearq[18:22]
        mano = int(vsano)
        svid = str(vid).zfill(6)
        for mmes in range(1, 13):
            mudia = calendar.monthrange(mano, mmes)[1]
            msmes = str(mano).zfill(4) + '-' + str(mmes).zfill(2)
            mdiainicio = 1
            mdiafim = mudia
            minicio = msmes + '-' + str(mdiainicio).zfill(2)
            mfim = msmes + '-' + str(mdiafim).zfill(2)
            logs('licitacoes', 'Iniciou download mês ' + str(mmes) + ' - ' + svid)
            if not os.path.exists('./static/json/licitacoes/'+ano+'/mensal/'):
                os.mkdir('./static/json/licitacoes/'+ano+'/mensal/')
            url = 'http://compras.dados.gov.br/' + 'licitacoes' + '/v1/' + 'licitacoes' + '.json?uasg=' + str(vid) + \
                  '&data_publicacao_min=' + minicio + '&data_publicacao_max=' + mfim
            logs('licitacoes', url)
            marquivo = 'licitacoes-' + svid + '-' + msmes + '.json'
            mpatharquivom = './static/json/licitacoes/'+ano+'/mensal/' + marquivo
            if not os.path.exists(mpatharquivom):
                request_json(url, 'licitacoes/'+ano+'/mensal', marquivo)
    if recursivo == 'S':
        baixa_uasg_mensal_diario_geral(ano)
    return True


def baixa_json_licitacao_uasg_anual_geral(vano, recursivo):
    tipo = 'licitacoes/'+vano
    from sqlalchemy import text

    t = text(" id "
             "FROM uasg "
             "where ativo"
             )

    uasgs = db.session.query(t).all()
   # query = db.session.query(Uasg).filter_by(Uasg.ativo == 1).query

    #uasgs = [row.uasg for row in query1.all()]

    #itemprecopraticado = Itensprecospraticados.query.filter_by(uasg=df_licitacao['uasg'],
    #                                                           modalidade=df_licitacao['modalidade'],
    #                                                           numero_aviso=df_licitacao['numero_aviso'],
    #                                                           numero_item_licitacao=df_licitacao[
    #                                                               'numero_item_licitacao']
    #                                                           ).first()
    numu = len(uasgs)
    u = 0
    for uasg in uasgs:
        u = u + 1
        vid = uasg[0]
        print('baixando Json de  licitacoes por Uasg do ano de '+vano+' ' + str(u) + '/' + str(numu))
        inicio = vano + '-01-01'
        fim = vano + '-12-31'
        logs('licitacoes', 'Iniciou download anual geral ' + vano + ' - ' + str(vid))
        if not os.path.exists('./static/json/licitacoes/'+vano):
            os.mkdir('./static/json/licitacoes/'+vano)
        url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?uasg=' + str(vid) + \
              '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
        logs('licitacoes', url)
        arquivo = 'licitacoes-' + str(vid).zfill(6) + '-' + vano + '.json'
        patharquivo = './static/json/licitacoes/' + vano + '/' + arquivo
        if not os.path.exists(patharquivo):
            request_json(url, tipo, arquivo)
    if recursivo == 'S':
        baixa_uasg_mensal_geral(vano, recursivo)
    return True
