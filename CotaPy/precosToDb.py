from sqlalchemy import create_engine
import os
import json
from sqlalchemy.dialects.mysql import insert
import pandas as pd2

vtabela = 'itensPrecoPraticado'


def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)


sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

# specify your path of directory
path = "..\\Novembro-2022\\precospraticados"

directories = os.listdir(path)
i = 1
for file in directories:
    nomearq = file
    print(str(i) + " - " + nomearq)
    try:
        with open(path + "\\" + nomearq, encoding="utf8") as json_file:
            data_json = json.loads(json_file.read())
    except:
        print("Erro na abertura do arquivo " + nomearq)
    try:
        embedded = data_json["_embedded"]
        tb = embedded['itensPrecoPraticado']
    except:
        print("Erro na preparação do " + nomearq)
    try:
        df = pd2.DataFrame.from_dict(tb, orient='columns')
        if '_links' in df.columns:
            del df['_links']
    except:
        print("Erro na leitura do " + nomearq)
    try:
        df.to_sql(vtabela, sqlEngine, if_exists='append', index=False, method=insert_on_duplicate)
    except:
        print("Erro na gravação do arquivo " + nomearq)
    i = i + 1