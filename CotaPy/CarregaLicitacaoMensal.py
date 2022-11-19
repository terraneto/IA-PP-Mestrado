import os
import json
import pandas as pd2

import ConectDB
from funcoes import insert_on_duplicate

sqlEngine= ConectDB.Conecte()

vtabela='licitacoes'
vtabelasiasg='licitacoes'

path = "..\\Novembro-2022\\Licitacoes"

directories = os.listdir(path)
i = 1
for file in directories:
    nomearq = file
    print(str(i) + " " + nomearq)
    try:
        with open(path + "\\" + nomearq, encoding="utf8") as json_file:
            data_json = json.loads(json_file.read())
    except:
        print("Erro na abertura do arquivo " + nomearq)
    try:
        embedded = data_json["_embedded"]
        count = data_json["count"]
        tb = embedded['licitacoes']
    except:
        print("Erro na preparação do " + nomearq)
    try:
        if count > 0:
            df = pd2.DataFrame.from_dict(tb, orient='columns')
            del df['_links']
            if 'numero_item_licitacao' in df.columns:
                del df['numero_item_licitacao']
            if 'codigo_do_item_no_catalogo' in df.columns:
                del df['codigo_do_item_no_catalogo']
    except:
        print("Erro na leitura do " + nomearq)
    try:
        if count>0:
            df.to_sql('licitacoes', sqlEngine, if_exists='append', index=False, method=insert_on_duplicate)
            if count >= 500:
                print("Maior que 500")
    except:
        print("Erro na gravação do arquivo " + nomearq)
    i = i + 1


