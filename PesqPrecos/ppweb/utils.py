import calendar
import datetime
import requests
import json
import os
import pandas as pd2

from ppweb.contratosdf import create_contratos_from_dataframe
from ppweb.fornecedoresdf import create_ambitos_ocorrencia_from_dataframe, create_cnaes_from_dataframe, \
    create_municipios_from_dataframe
from ppweb.licitacoesdf import create_uasg_from_dataframe, create_orgaos_from_dataframe
from ppweb.materiaisdf import create_classes_from_dataframe, create_grupos_from_dataframe, \
    create_materiais_from_dataframe, create_pdms_from_dataframe


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


def carrega_json(tipo):
    path = './static/json/' + tipo
    directories = os.listdir(path)
    i = 1
    for file in directories:
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
            embedded = data_json["_embedded"]
            if tipo == "ambitos_ocorrencia":
                tb = embedded["AmbitosOcorrencia"]
            else:
                tb = embedded[tipo]
            df = pd2.DataFrame.from_dict(tb, orient='columns')
            match tipo:
                case "uasgs":
                    create_uasg_from_dataframe(df)
                case "Orgaos":
                    create_orgaos_from_dataframe(df)
                case "classes":
                    create_classes_from_dataframe(df)
                case "grupos":
                    create_grupos_from_dataframe(df)
                case "materiais":
                    create_materiais_from_dataframe(df)
                case "pdms":
                    create_pdms_from_dataframe(df)
                case "ambitos_ocorrencia":
                    create_ambitos_ocorrencia_from_dataframe(df)
                case "cnaes":
                    create_cnaes_from_dataframe(df)
                case "municipios":
                    create_municipios_from_dataframe(df)
                case "contratos":
                    create_contratos_from_dataframe(df)
                case _:
                    print('default')
        except Exception as excecao:
            print("Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
        i = i + 1
    return True


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
        # if ptipo == 'materiais' and pag < 3234:
        #   pag = 3400
        #   numpags = 3452
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


def baixa_json_contratos_mensal(modulo, ptipo, vano):
    ano = int(vano)
    print('baixa Json ' + modulo + ' - ' + ptipo)
    for mes in range(1, 13):
        udia = calendar.monthrange(ano, mes)[1]
        udia1 = udia + 1
        print(udia1)
        smes = str(ano).zfill(4) + '-' + str(mes).zfill(2)
        inicio = smes + '-' + str(1).zfill(2)
        fim = smes + '-' + str(udia).zfill(2)
        pag = 0
        numpags = 1
        logs(ptipo, 'Iniciou download mês ' + str(mes) + ' número páginas=' + str(numpags))
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


def baixa_material_por_id():
    numpags = 1730000
    ptipo = 'material'
    if not os.path.exists('./static/json/material'):
        os.mkdir('./static/json/material')
    for ident in range(1, numpags):
        arquivo = 'material' + str(ident).zfill(7) + '.json'
        patharquivo = './static/json/material/' + arquivo
        url = 'http://compras.dados.gov.br/materiais/id/material/' + str(ident) + '.json'
        if os.path.exists(patharquivo):
            logs(ptipo, 'Pulou pagina=' + str(ident))
            continue
        baixou = request_json(url, ptipo, arquivo)
        if baixou:
            print('baixada ' + str(ident) + '/' + str(numpags))
            logs(ptipo, 'Terminou paginas=' + str(ident))
            logs(ptipo, 'número paginas=' + str(numpags))
    return True
