import datetime
import requests
import json
import os
from ppweb.ext.database import db
import pandas as pd2

from ppweb.models import Uasg, Orgao


def request_json(url, tipo, arquivo):
    temparquivo = './static/json/' + tipo + '/temp' + arquivo
    patharquivo = './static/json/' + tipo + '/' + arquivo
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


def baixa_json_baselicitacoes(tipo, parametro):
    pag = 0
    numpags = 1
    logs(tipo, 'Iniciou download número páginas=' + str(numpags))
    while pag < numpags:
        valpag = 500 * pag
        if parametro is None:
            url = 'http://compras.dados.gov.br/licitacoes/v1/' + tipo + '.json?offset=' + str(valpag)
        else:
            url = 'http://compras.dados.gov.br/licitacoes/v1/' + tipo + '.json?' + parametro + '&offset=' + str(valpag)
        print(url)
        arquivo = tipo + str(valpag) + '.json'
        if os.path.exists('./static/json/' + tipo + '/' + arquivo) and pag > 0:
            pag += 1
            logs(tipo, 'Pulou pagina=' + str(pag))
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
        logs(tipo, 'Terminou paginas=' + str(pag))
        logs(tipo, 'número paginas=' + str(numpags))
    return True


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
            tb = embedded[tipo]
            df = pd2.DataFrame.from_dict(tb, orient='columns')
            match tipo:
                case "uasgs":
                    create_uasg_from_dataframe(df)
                case "Orgaos":
                    create_orgaos_from_dataframe(df)
                case _:
                    print('default')
        except Exception as excecao:
            print("Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
        i = i + 1
    return True


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
                Orgao.verified = True
            else:
                db.session.add(orgao)
        db.session.commit()
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def baixa_json_basemateriais(tipo, parametro):
    pag = 0
    numpags = 1
    logs(tipo, 'Iniciou download número páginas=' + str(numpags))
    while pag < numpags:
        valpag = 500 * pag
        if parametro is None:
            url = 'http://compras.dados.gov.br/materiais/v1/' + tipo + '.json?offset=' + str(valpag)
        else:
            url = 'http://compras.dados.gov.br/materiais/v1/' + tipo + '.json?' + parametro + '&offset=' + str(valpag)
        print(url)
        arquivo = tipo + str(valpag) + '.json'
        if os.path.exists('./static/json/' + tipo + '/' + arquivo) and pag > 0:
            pag += 1
            logs(tipo, 'Pulou pagina=' + str(pag))
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
        logs(tipo, 'Terminou paginas=' + str(pag))
        logs(tipo, 'número paginas=' + str(numpags))
    return True