import json
import os
import pandas as pd2
from ppweb.contratosdf import create_contratos_from_dataframe, create_itenscontratos_from_dataframe
from ppweb.fornecedoresdf import create_ambitos_ocorrencia_from_dataframe, create_cnaes_from_dataframe, \
    create_municipios_from_dataframe, create_fornecedores_from_dataframe
from ppweb.licitacoesdf import create_uasg_from_dataframe, create_orgaos_from_dataframe, \
    create_licitacoes_from_dataframe, create_itenslicitacao_from_dataframe, create_itensprecospraticados_from_dataframe
from ppweb.materiaisdf import create_classes_from_dataframe, create_grupos_from_dataframe, \
    create_materiais_from_dataframe, create_pdms_from_dataframe
from ppweb.utils import logs


def carrega_json(tipo):
    path = './static/json/' + tipo
    directories = os.listdir(path)
    i = 0
    numdir = len(directories)
    for file in directories:
        i = i+1
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
                    case _:
                        tb = embedded[tipo]
                df = pd2.DataFrame.from_dict(tb, orient='columns')
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
                    case _:
                        print('default')
        except Exception as excecao:
            print("Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
            logs(tipo, "Erro na gravação do arquivo " + str(excecao.__cause__) + nomearq)
    return True
