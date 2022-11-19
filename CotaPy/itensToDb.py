import os
from sqlalchemy import create_engine
from funcoes import carrega_json_sql

vtabela = 'itensLicitacao'

sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

# specify your path of directory
path = "..\\Novembro-2022\\itensPY"

directories = os.listdir(path)
i = 1
for file in directories:
    print(str(i) + " " + file)
    carrega_json_sql(path, file, sqlEngine, vtabela, vtabela)
    i = i + 1
