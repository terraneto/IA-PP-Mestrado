import datetime
import requests
import json
import os
import pandas as pd2
import ast

from ppweb.fornecedoresdf import create_fornecedores_from_dataframe
from ppweb.materiaisdf import create_materiais_from_dataframe
from ppweb.models import Licitacao, Pregao


def request_json(url, tipo, arquivo):
    temparquivo = './static/json/' + tipo + '/temp' + arquivo
    patharquivo = './static/json/' + tipo + '/' + arquivo
    status = False
    erro = 0
    tempo = 5
    while status is False and erro < 3:
        try:
            data = datetime.datetime.now()
            str_now = data.strftime('%Y-%m-%d %H:%M:%S')
            mensagem = 'Request_json - ' + tipo + ' - ' + str_now + ' - Baixando ' + url + ' Erro=' + str(erro)
            logs(tipo, mensagem)
            response = requests.get(url, timeout=tempo)
            mensagem = 'Request_json - ' + tipo + ' - Status do download ' + str(response.status_code)
            logs(tipo, mensagem)
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
                    logs(tipo, response.headers.get('content-type'))
            else:
                if response.status_code == 404:
                    return False
        except (requests.exceptions.RequestException, ValueError) as e:
            print(e)
        finally:
            erro = erro + 1
    return status


def request_json_naosobrepoe(url, tipo, arquivo):
    patharquivo = './static/json/' + tipo + '/' + arquivo
    status = False
    erro = 0
    tempo = 5
    while status is False and erro < 3:
        try:
            if os.path.exists(patharquivo):
                return True
            response = requests.get(url, timeout=tempo)
            if response.status_code == 200:
                if response.headers.get('content-type') == 'application/json':
                    data_json = response.json()
                    with open(patharquivo, 'w') as f:
                        json.dump(data_json, f)
                    return True
            else:
                if response.status_code == 404:
                    return False
        except (requests.exceptions.RequestException, ValueError) as e:
            print(e)
        finally:
            erro = erro + 1
    return status


def logs(tipo, mensagem):
    data = datetime.datetime.now()
    if not os.path.exists('./static/logs/' + tipo):
        os.mkdir('./static/logs/' + tipo)
    log = './static/logs/' + tipo + '/' + data.strftime('%Y-%m-%d') + '.txt'
    f = open(log, 'a+', encoding="utf8")
    mensagem = data.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + mensagem + '\n'
    f.write(mensagem)
    f.close()


def baixa_json(modulo, ptipo):
    print('baixa Json ' + modulo + ' - ' + ptipo)
    pag = 0
    numpags = 1
    logs(ptipo, 'Iniciou download número páginas=' + str(numpags))
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    while pag < numpags:
        valpag = 500 * pag
        url = 'http://compras.dados.gov.br/' + modulo + '/v1/' + ptipo + '.json?offset=' + str(valpag)
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
        baixou = request_json_naosobrepoe(url, ptipo, arquivo)
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
    return str(numpags)


def baixa_json_material(material):
    print('Iniciando busca de material')
    modulo = 'materiais'
    ptipo = 'material'
    print('baixa Json ' + modulo + ' - ' + ptipo)
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    url = 'http://compras.dados.gov.br/' + modulo + '/id/' + ptipo + '/' + str(material).zfill(7) + '.json'
    arquivo = ptipo + str(material).zfill(7) + '.json'
    patharquivo = './static/json/' + ptipo + '/' + arquivo
    print(url)
    baixou = request_json_naosobrepoe(url, ptipo, arquivo)
    material = None
    if baixou:
        with open(patharquivo, encoding="utf8") as jsonfile:
            data_json = json.loads(jsonfile.read())
        print(data_json)
        df = pd2.DataFrame.from_dict(data_json, orient='columns')
        material = create_materiais_from_dataframe(df)
    return material


def baixa_json_fornecedor_pj(cnpj_fornecedor):
    print('Iniciando busca de fornecedor')
    modulo = 'fornecedores'
    ptipo = 'fornecedor_pj'
    print('baixa Json ' + modulo + ' - ' + ptipo)
    if not os.path.exists('./static/json/' + ptipo):
        os.mkdir('./static/json/' + ptipo)
    url = 'http://compras.dados.gov.br/' + modulo + '/id/' + ptipo + '/' + str(cnpj_fornecedor).zfill(14) + '.json'
    arquivo = ptipo + str(cnpj_fornecedor).zfill(14) + '.json'
    patharquivo = './static/json/' + ptipo + '/' + arquivo
    print(url)
    baixou = request_json_naosobrepoe(url, ptipo, arquivo)
    fornecedor = None
    if baixou:
        with open(patharquivo, encoding="utf8") as jsonfile:
            data_json = json.loads(jsonfile.read())
        print(data_json)
        df = pd2.DataFrame.from_dict(data_json, orient='columns')
        fornecedor = create_fornecedores_from_dataframe(df)
    return fornecedor


def baixa_json_pregoes():
    print('baixa Json licitacoes - pregões')
    licitacoes = Licitacao.query.with_entities(Licitacao.uasg, Licitacao.numero_aviso).filter_by(
        modalidade=5).distinct().all()
    i = 0
    for licitacao in licitacoes:
        i = i + 1
        id_pregao = str(int(licitacao.uasg)).zfill(6) + str(int(licitacao.numero_aviso)).zfill(10)
        url = 'http://compras.dados.gov.br/pregoes/id/pregao/' + id_pregao + '.json'
        arquivo = 'pregao' + id_pregao + '.json'
        patharquivo = './static/json/pregao/' + arquivo
        if os.path.exists(patharquivo):
            continue
        erro = 0
        print('********\n', 'processando pregão ' + str(i) + ' de ' + str(len(licitacoes)))
        print(url)
        while erro < 3:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    if response.headers.get('content-type') == 'application/json':
                        data_json = response.json()
                        dados = str(data_json)
                        dados = '[' + dados[0:dados.find("_links") - 2] + '}]'
                        data_json = ast.literal_eval(dados)
                        with open(patharquivo, 'w') as f:
                            json.dump(data_json, f)
            except (requests.exceptions.RequestException, ValueError) as e:
                print(e)
            finally:
                erro = erro + 1


def baixa_json_itens_pregoes():
    print('baixa Json Itens de pregões')
    pregoes = Pregao.query.all()
    i = 0
    for pregao in pregoes:
        i = i + 1
        id_pregao = pregao.numero
        url = 'http://compras.dados.gov.br/pregoes/id/pregao/' + str(id_pregao).zfill(16) + '/itens.json'
        arquivo = 'itenspregao' + str(id_pregao).zfill(16) + '.json'
        patharquivo = './static/json/itenspregao/' + arquivo
        if os.path.exists(patharquivo):
            continue
        erro = 0
        print('********\n', 'processando itens do pregão ' + str(i) + ' de ' + str(len(pregoes)))
        print(url)
        while erro < 3:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    if response.headers.get('content-type') == 'application/json':
                        data_json = response.json()
                        with open(patharquivo, 'w') as f:
                            json.dump(data_json, f)
            except (requests.exceptions.RequestException, ValueError) as e:
                print(e)
            finally:
                erro = erro + 1
