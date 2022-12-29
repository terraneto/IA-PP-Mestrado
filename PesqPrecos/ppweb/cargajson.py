import json
import os
import pandas as pd2
from ppweb.contratosdf import create_contratos_from_dataframe
from ppweb.fornecedoresdf import create_ambitos_ocorrencia_from_dataframe, create_cnaes_from_dataframe, \
    create_municipios_from_dataframe
from ppweb.licitacoesdf import create_uasg_from_dataframe, create_orgaos_from_dataframe, \
    create_licitacoes_from_dataframe
from ppweb.materiaisdf import create_classes_from_dataframe, create_grupos_from_dataframe, \
    create_materiais_from_dataframe, create_pdms_from_dataframe
from ppweb.utils import logs


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
            numero = data_json["count"]
            print('registros no arquivo='+str(numero))
            if numero > 0:
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
                    case "licitacoes":
                        print('Licitacoes - arquivo='+str(file))
                        create_licitacoes_from_dataframe(df)
                    case _:
                        print('default')
        except Exception as excecao:
            print("Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
            logs(tipo, "Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
        i = i + 1
    return True
