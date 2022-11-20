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

frame = pd.read_sql('SELECT * FROM siasg.Bancodeteste where codigo_pdm=06661', dbConnection)
frame.to_sql('computadores', dbConnection, if_exists='append', index=False, method=insert_on_duplicate)

frame = pd.read_sql('SELECT * FROM siasg.Bancodeteste where codigo_pdm=08435', dbConnection)
frame.to_sql('notebooks', dbConnection, if_exists='append', index=False, method=insert_on_duplicate)