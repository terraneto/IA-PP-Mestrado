# SELECT distinct codigo_item_material FROM siasg.itensLicitacao where !(codigo_item_material is null);
# http://compras.dados.gov.br/materiais/id/material/000227505.json
# str(num).zfill(9)

from sqlalchemy import create_engine
import pandas as pd
import os


from funcoes import request_json

print('Comecei')
sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

# specify your path of directory
path = "..\\Novembro-2022\\material"

vtabela = 'licitacoes'
qsql = 'SELECT distinct codigo_item_material FROM'
qsql = qsql + ' siasg.itensLicitacao where codigo_item_material is not null order by codigo_item_material'

frame = pd.read_sql(qsql, dbConnection)
print(frame)
for row in frame.codigo_item_material:
    nomearq = 'material' + str(row).zfill(9) + '.json'
    arquivo = path + "\\" + nomearq
    if row < 11800:
        continue
    if not (os.path.exists(arquivo)):
        print('Fazendo ' + str(row))
        url = 'http://compras.dados.gov.br/materiais/id/material/' + str(row).zfill(9) + '.json'
        request_json(url, path + "\\" + nomearq)
print('Concluído')
