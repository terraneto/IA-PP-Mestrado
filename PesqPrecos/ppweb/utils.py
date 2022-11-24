import requests
import json
import os


def request_json(url, tipo, arquivo):
    temparquivo = './static/json/' + tipo +'/temp' + arquivo
    patharquivo = './static/json/' + tipo +'/'+ arquivo
    try:
        response = requests.get(url)
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
                return False
        else:
            print(response.status_code)
            return False
    except (requests.exceptions.RequestException, ValueError) as e:
        print(e)
        return False


def baixa_json_baselicitacoes(tipo):
    pag = 0
    numpags = 1
    while pag < numpags:
        valpag = 500 * pag
        url = 'http://compras.dados.gov.br/licitacoes/v1/' + tipo + '.json?offset=' + str(valpag)
        arquivo = tipo + str(valpag) + '.json'
        if os.path.exists('./static/json/' + tipo + '/' + arquivo):
            pag += 1
            continue
        baixou = request_json(url, tipo, arquivo)
        if baixou:
            with open('./static/json/' + tipo + '/' + arquivo) as jsonfile:
                data_json = json.load(jsonfile)
                num = data_json["count"]
                totalpag = num // 500
                if num % 500 > 0:
                   totalpag = totalpag + 1
                numpags = totalpag
        pag += 1
    return True


