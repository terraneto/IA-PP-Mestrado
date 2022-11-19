import os
from sqlalchemy import create_engine
import pandas as pd

from funcoes import request_json

sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

path = "..\\Novembro-2022\\precospraticados"

vtabela = 'licitacoes'
frame = pd.read_sql('select distinct identificador from licitacoes', dbConnection)
query = 'select count(*) from ' + vtabela
try:
    numero = pd.read_sql(query, dbConnection)
    n = numero['count(*)'][0]
except:
    n = 0
print(n)
reg = 0
while reg < n:
    nomearq = path + '\\precospraticados' + frame['identificador'][reg] + '.json'
    if not (os.path.exists(nomearq)):
        url = 'http://compras.dados.gov.br/licitacoes/id/preco_praticado/' + frame['identificador'][reg] + '/itens.json'
        response = request_json(url, nomearq)
    reg += 1
    print(reg)
