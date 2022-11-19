import json
import requests
from sqlalchemy.dialects.mysql import insert


def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)


def request_json(url, arquivo):
    print('Inicio request_json url=' + url + ' arquivo=' + arquivo)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.headers.get('content-type') == 'application/json':
                data_json = response.json()
                with open(arquivo, 'w') as f:
                    json.dump(data_json, f)
                return True
            else:
                print(response.headers.get('content-type'))
                return False
        else:
            print(response.status_code)
            return False
    except (requests.exceptions.RequestException, ValueError) as e:
        print(e)
        return False


