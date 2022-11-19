from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
import pandas as pd
import pandas as pd2


def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)


sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
dbConnection = sqlEngine.connect()

frame = pd.read_sql('SELECT * FROM siasg.itensPrecoPraticado where !(codigo_item_material is null)', dbConnection)
for index, row in frame.iterrows():
    cod = row['codigo_item_material']
    frame2 = pd2.read_sql('SELECT id_classe, id_pdm, descricao from siasg.materiais where codigo=' + str(cod),
                          dbConnection)
    if frame2.size > 0:
        classe = frame2['id_classe'][0]
        pdm = frame2['id_pdm'][0]
        descricao = frame2['descricao'][0]
    else:
        classe = 0
        pdm = 0
        descricao = ''
    frame.at[index, 'codigo_pdm'] = pdm
    frame.at[index, 'codigo_classe'] = classe
    frame.at[index, 'descricao_material'] = descricao
    # ######################  Descritor PDM
    frame2 = pd2.read_sql('SELECT descricao from siasg.pdms where codigo=' + str(pdm), dbConnection)
    if frame2.size > 0:
        descricao = frame2['descricao'][0]
    else:
        descricao = ''
    frame.at[index, 'descricao_pdm'] = descricao
    print(str(index) + ' concluído')
frame.to_sql('Bancodetestepp', dbConnection, if_exists='append', index=False, method=insert_on_duplicate)
