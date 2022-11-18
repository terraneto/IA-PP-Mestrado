import json
import requests
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from sqlalchemy import insert


def baixar_json(url, arquivo):
    print('Inicio baixar_json url=' + url + ' arquivo=' + arquivo)
    try:
        response = urlopen(url)
        data_json = json.loads(response.read())
        with open(arquivo, 'w') as f:
            json.dump(data_json, f)
        return True
    except HTTPError as e:
        print('Erro' + str(e.code))
        return False
    except URLError as u:
        print('Erro de URL' + str(u.errno))
        return False


def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)


def request_json(url, arquivo):
    print('Inicio request_json url=' + url + ' arquivo=' + arquivo)
    response = requests.get(url)
    if response.status_code == 200:
        resposta = response.content
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
