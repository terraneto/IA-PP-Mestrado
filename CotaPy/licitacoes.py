import calendar
import os

from funcoes import baixar_json

# specify your path of directory
path = "..\\Novembro-2022\\Licitacoes - Diarias"
anos: list[int] = [2021, 2022]

vtabela = 'licitacoes'
for ano in anos:
    for mes in range(1, 13):
        udia = calendar.monthrange(ano, mes)[1]
        udia1 = udia + 1
        print(udia1)
        for dia in range(1, udia1):
            erro: bool = True
            while erro:
                sdia = str(ano).zfill(4) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2)
                sudia = str(ano).zfill(4) + '-' + str(mes).zfill(2) + '-' + str(udia).zfill(2)
                nomearq = 'licitacoes' + sdia + '.json'
                arquivo = path + "\\" + nomearq
                print(arquivo)
                if not (os.path.exists(arquivo)):
                    print('Fazendo ' + sdia)
                    url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?data_publicacao=' + sdia
                    arquivo = path + "\\" + nomearq
                    erro = not baixar_json(url, arquivo)
print('Concluído')
