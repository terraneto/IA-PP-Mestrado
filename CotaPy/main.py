import os
from sqlalchemy import create_engine
from dateutil.relativedelta import *
from datetime import date
import json
import pandas as pd2

from funcoes import insert_on_duplicate

if __name__ == '__main__':
    print('PyCharm')

sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

arquivos: int = 10
datainicio: date = date(2022, 10, 1)
print(datainicio)

vtabela = 'licitacoesmes'
vtabelasiasg = 'licitacoes'

while arquivos > 0:
    nomearq = '..\\Novembro-2022\\licitacoes\\' + vtabelasiasg + datainicio.strftime("%Y-%m") + '.json'
    print(nomearq)
    try:
        with open(nomearq, encoding="utf8") as json_file:
            data_json = json.loads(json_file.read())
    except:
        print("Erro na abertura do arquivo" + nomearq)
    try:
        embedded = data_json["_embedded"]
        tb = embedded[vtabelasiasg]
    except:
        print("Erro na preparação do " + nomearq)
    try:
        df = pd2.DataFrame.from_dict(tb, orient='columns')
        del df['_links']
        if 'numero_item_licitacao' in df.columns:
            del df['numero_item_licitacao']
        if 'codigo_do_item_no_catalogo' in df.columns:
            del df['codigo_do_item_no_catalogo']
    except:
        print("Erro na leitura do " + nomearq)
    df.to_sql(vtabela, sqlEngine, if_exists='append', index=False, method=insert_on_duplicate)
    datainicio = datainicio - relativedelta(months=1)
    print(datainicio)
    arquivos = arquivos - 1

# specify your path of directory
path = "..\\Novembro-2022\\Licitacoes - Dia"

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
            df.to_sql('licitacoesdia', sqlEngine, if_exists='append', index=False, method=insert_on_duplicate)
            if count >= 500:
                print("Maior que 500")
    except:
        print("Erro na gravação do arquivo " + nomearq)
    i = i + 1

