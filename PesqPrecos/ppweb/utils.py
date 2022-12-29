import calendar
import datetime
import requests
import json
import os

from ppweb.ext.database import db
from ppweb.models import Uasg, Licitacao


def request_json(url, tipo, arquivo):
    temparquivo = './static/json/' + tipo + '/temp' + arquivo
    patharquivo = './static/json/' + tipo + '/' + arquivo
    status = False
    erro = 0
    tempo = 40
    while status is False and erro < 2:
        try:
            data = datetime.datetime.now()
            str_now = data.strftime('%Y-%m-%d %H:%M:%S')
            print('Request_json - ' + tipo + ' - ' + str_now + ' - Baixando ' + url + ' Erro=' + str(erro))
            response = requests.get(url, timeout=tempo)
            print('Request_json - ' + tipo + ' - Status do download ' + str(response.status_code))
            if response.status_code == 200:
                if response.headers.get('content-type') == 'application/json':
                    data_json = response.json()
                    with open(temparquivo, 'w') as f:
                        json.dump(data_json, f)
                    if os.path.exists(patharquivo):
                        if os.path.getsize(temparquivo) > os.path.getsize(patharquivo):
                            os.remove(patharquivo)
                            os.rename(temparquivo, patharquivo)
                        else:
                            os.remove(temparquivo)
                    else:
                        os.rename(temparquivo, patharquivo)
                    return True
                else:
                    print(response.headers.get('content-type'))
            else:
                if response.status_code == 404:
                    return False
        except (requests.exceptions.RequestException, ValueError) as e:
            print(e)
            tempo = tempo + 10
        finally:
            erro = erro + 1
    return status


def logs(tipo, mensagem):
    data = datetime.datetime.now()
    str_now = data.strftime('%Y-%m-%d %H:%M:%S')
    sodata = data.strftime('%Y-%m-%d')
    log = './static/logs/' + tipo + sodata + '.txt'
    f = open(log, 'a+', encoding="utf8")
    f.write(str_now + ' - ' + mensagem + '\n')
    f.close()


def baixa_json(modulo, ptipo, tparametro):
    print('baixa Json ' + modulo + ' - ' + ptipo)
    pag = 0
    numpags = 1
    logs(ptipo, 'Iniciou download número páginas=' + str(numpags))
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    while pag < numpags:
        valpag = 500 * pag
        if tparametro is None:
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?offset=' + str(valpag)
        else:
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?' + tparametro + \
                  '&offset=' + str(valpag)
        arquivo = ptipo + str(valpag) + '.json'
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
                    os.rename(oldarquivo, patharquivo)
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


def baixa_json_mensal(modulo, ptipo, vano):
    ano = int(vano)
    print('baixa Json ' + modulo + ' - ' + ptipo)
    for mes in range(1, 13):
        udia = calendar.monthrange(ano, mes)[1]
        smes = str(ano).zfill(4) + '-' + str(mes).zfill(2)
        for parte in range(1, 32):
            diainicio = parte
            diafim = parte + 1
            if diafim > udia:
                diafim = udia
            inicio = smes + '-' + str(diainicio).zfill(2)
            fim = smes + '-' + str(diafim).zfill(2)
            pag = 0
            numpags = 1
            logs(ptipo,
                 'Iniciou download mês ' + str(mes) + ' - parte ' + str(parte) + ' número páginas=' + str(numpags))
            if not os.path.exists('./static/json/' + ptipo):
                os.mkdir('./static/json/' + ptipo)
            while pag < numpags:
                valpag = 500 * pag
                if ptipo == 'licitacoes':
                    url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?' + \
                          'data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim + '&offset=' + str(valpag)

                else:
                    url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?' + \
                          'data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim + '&offset=' + str(valpag)
                print(url)
                arquivo = ptipo + smes + '-' + str(parte) + '-' + str(valpag).zfill(4) + '.json'
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


def baixa_json_diario(modulo, ptipo, vano):
    print('baixa Json ' + modulo + ' - ' + ptipo)
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    for mes in range(1, 13):
        udia = calendar.monthrange(int(vano), mes)[1]
        udia1 = udia + 1
        print(udia)
        logs(ptipo, 'Iniciou download mês ' + str(mes))
        for dia in range(1, udia1):
            pag = 0
            numpags = 1
            while pag < numpags:
                valpag = 500 * pag
                sdia = str(vano).zfill(4) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2)
                arquivo = ptipo + sdia + '-' + str(valpag).zfill(4) + '.json'
                patharquivo = './static/json/' + ptipo + '/' + arquivo
                oldarquivo = './static/json/' + ptipo + '/old' + arquivo
                url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?' + \
                      'data_publicacao=' + sdia + '&offset=' + str(valpag)
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


def baixa_json_uasg_mensal(modulo, ptipo, vano):
    uasgs = Uasg.query.all()
    for uasg in uasgs:
        vid = uasg.id
        ano = int(vano)
        print('baixa Json ' + modulo + ' - ' + ptipo)
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
                 'Iniciou download mês ' + str(mes) + ' - ' + str(vid) + ' número páginas='
                 + str(numpags))
            if not os.path.exists('./static/json/' + ptipo):
                os.mkdir('./static/json/' + ptipo)
            while pag < numpags:
                valpag = 500 * pag
                if ptipo == 'licitacoes':
                    url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                          '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim + '&offset=' + \
                          str(valpag)
                else:
                    url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                          '&data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim + '&offset=' + \
                          str(valpag)
                print(url)
                arquivo = ptipo + smes + '-' + str(vid) + '-' + str(valpag).zfill(4) + '.json'
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


def baixa_uasg_mensal(uasg, vano, ptipo, modulo):
    vid = uasg.id
    ano = int(vano)
    print('baixa Json ' + modulo + ' - ' + ptipo)
    for mes in range(1, 13):
        udia = calendar.monthrange(ano, mes)[1]
        smes = str(ano).zfill(4) + '-' + str(mes).zfill(2)
        diainicio = 1
        diafim = udia
        inicio = smes + '-' + str(diainicio).zfill(2)
        fim = smes + '-' + str(diafim).zfill(2)
        logs(ptipo, 'Iniciou download mês ' + str(mes) + ' - ' + str(vid))
        if not os.path.exists('./static/json/' + ptipo):
            os.mkdir('./static/json/' + ptipo)
        if ptipo == 'licitacoes':
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                  '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
        else:
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                  '&data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim
        print(url)
        arquivo = ptipo + smes + '-' + str(vid) + '.json'
        request_json(url, ptipo, arquivo)
    return True


def baixa_json_uasg_anual(modulo, ptipo, vano):
    uasgs = Uasg.query.all()
    for uasg in uasgs:
        vid = uasg.id
        print('baixa Json ' + modulo + ' - ' + ptipo)
        inicio = vano + '-01-01'
        fim = vano + '-12-31'
        logs(ptipo, 'Iniciou download anual ' + vano + ' - ' + str(vid))
        if not os.path.exists('./static/json/' + ptipo):
            os.mkdir('./static/json/' + ptipo)
        if ptipo == 'licitacoes':
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                  '&data_publicacao_min=' + inicio + '&data_publicacao_max=' + fim
        else:
            url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?uasg=' + str(vid) + \
                  '&data_assinatura_min=' + inicio + '&data_assinatura_max=' + fim
        print(url)
        arquivo = ptipo + vano + '-' + str(vid) + '.json'
        patharquivo = './static/json/' + ptipo + '/' + arquivo
        if not os.path.exists(patharquivo):
            baixou = request_json(url, ptipo, arquivo)
            if baixou:
                with open(patharquivo) as jsonfile:
                    data_json = json.load(jsonfile)
                    num = data_json["count"]
                    totalpag = num // 500
                    if (totalpag == 1) and (num % 500 == 0):
                        baixa_uasg_mensal(uasg, vano, ptipo, modulo)
    return True


def baixa_json_itenslicitacoes():
    identificadores = db.session.query(Licitacao.identificador).distinct().all()
    for licitacao in identificadores:
        print('baixando itens')
        if not os.path.exists('./static/json/itenslicitacoes'):
            os.mkdir('./static/json/itenslicitacoes')
        url = 'http://compras.dados.gov.br/licitacoes/id/licitacao/'+licitacao.identificador+'/itens.json'
        print(url)
        arquivo = licitacao.identificador + '.json'
        patharquivo = './static/json/itenslicitacoes/' + arquivo
        if not os.path.exists(patharquivo):
            baixou = request_json(url, 'itenslicitacoes', arquivo)
    return True

