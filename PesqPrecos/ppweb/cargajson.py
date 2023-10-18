import json
import os
import pandas as pd2
from ppweb.contratosdf import create_contratos_from_dataframe, create_itenscontratos_from_dataframe
from ppweb.fornecedoresdf import create_ambitos_ocorrencia_from_dataframe, create_cnaes_from_dataframe, \
    create_municipios_from_dataframe, create_fornecedores_from_dataframe
from ppweb.licitacoesdf import create_uasg_from_dataframe, create_orgaos_from_dataframe, \
    create_licitacoes_from_dataframe, create_itenslicitacao_from_dataframe, \
    create_itensprecospraticados_from_dataframe
from ppweb.materiaisdf import create_classes_from_dataframe, create_grupos_from_dataframe, \
    create_materiais_from_dataframe, create_pdms_from_dataframe
from ppweb.pregoesdf import create_itenspregoes_from_dataframe, create_pregoes_from_dataframe
from ppweb.utils import logs


def carrega_json(tipo):
    path = './static/json/' + tipo
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Carregando arquivo ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
                embedded = data_json["_embedded"]
                numero = data_json["count"]
            if numero > 0:
                match tipo:
                    case "ambitos_ocorrencia":
                        tb = embedded["AmbitosOcorrencia"]
                    case "itenslicitacao":
                        tb = embedded["itensLicitacao"]
                    case "itenscontrato":
                        tb = embedded["itens_compras_contratos"]
                    case "itensprecospraticados":
                        tb = embedded["itensPrecoPraticado"]
                    case "itenspregoes":
                        tb = embedded["pregoes"]
                    case _:
                        tb = embedded[tipo]
                df = pd2.DataFrame.from_dict(tb, orient='columns')
                print(df)
                df2 = df.astype(object).where(pd2.notnull(df), None)
                df = df2
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
                    case "licitacoes":
                        create_licitacoes_from_dataframe(df)
                    case "itenslicitacao":
                        create_itenslicitacao_from_dataframe(df)
                    case "itenscontrato":
                        create_itenscontratos_from_dataframe(df)
                    case "itensprecospraticados":
                        create_itensprecospraticados_from_dataframe(df)
                    case "fornecedores":
                        create_fornecedores_from_dataframe(df)
                    case "pregoes":
                        create_pregoes_from_dataframe(df)
                    case "itenspregoes":
                        create_itenspregoes_from_dataframe(df)
                    case _:
                        print('default')
        except Exception as excecao:
            print("Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
            logs(tipo, "Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
    return True


def carrega_json_pregoes():
    path = './static/json/pregao'
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i + 1
        print('Carregando arquivo ' + str(i) + '/' + str(numdir))
        nomearq = file
        try:
            with open(path + "//" + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
                df = pd2.DataFrame.from_dict(data_json, orient='columns')
                df['numero'] = int(nomearq[6:22])
                df2 = df.astype(object).where(pd2.notnull(df), None)
                df = df2
                create_pregoes_from_dataframe(df)
        except Exception:
            print("Erro na importação do arquivo " + nomearq)
    return True


def carrega_json_licitacoes_ano(vano):
    path = './static/json/licitacoes/' + str(vano)
    if os.path.exists(path):
        carrega_json_licitacoes(path)
    pathm = path + '/mensal'
    if os.path.exists(pathm):
        carrega_json_licitacoes(pathm)
    pathd = path + '/diario'
    if os.path.exists(pathd):
        carrega_json_licitacoes(pathd)
    pathc = path + '/classes'
    if os.path.exists(pathc):
        carrega_json_licitacoes(pathc)
    pathma = path + '/materiais'
    if os.path.exists(pathma):
        carrega_json_licitacoes(pathma)


def carrega_json_licitacoes(path):
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        if os.path.isdir(file):
            continue
        i = i + 1
        print('Carregando arquivo ' + str(i) + '/' + str(numdir) + ' de ' + path)
        nomearq = file
        try:
            with open(path + '//' + nomearq, encoding="utf8") as json_file:
                data_json = json.loads(json_file.read())
            embedded = data_json["_embedded"]
            numero = data_json["count"]
            if numero > 0:
                tb = embedded["licitacoes"]
                df = pd2.DataFrame.from_dict(tb, orient='columns')
                df2 = df.astype(object).where(pd2.notnull(df), None)
                df = df2
                create_licitacoes_from_dataframe(df)
        except Exception as excecao:
            print("Erro na carga do arquivo " + str(excecao.__cause__) + nomearq)
    return True
