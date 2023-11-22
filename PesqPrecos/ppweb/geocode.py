from geopy import distance

from ppweb.models import Municipio


def recupera_localizacao(id_municipio):
    vid=id_municipio
    municipio = Municipio.query.filter_by(id=vid).first()
    try:
        localizacao = (municipio.latitude, municipio.longitude)
    except:
        localizacao = (0, 0)
    return localizacao


# se tiver alguma das cidades ou dados faltando a distância ficará igual a 0
def calcula_distancia(id_cidade1, id_cidade2):
    try:
        c1 = recupera_localizacao(id_cidade1)
        c2 = recupera_localizacao(id_cidade2)
        distancia = distance.distance(c1, c2).km
    except:
        distancia = 0.00
    return distancia


# se tiver alguma das cidades ou dados faltando a distância ficará igual a 0
def calcula_distancia_circunferencia(id_cidade1, id_cidade2):
    c1 = recupera_localizacao(id_cidade1)
    c2 = recupera_localizacao(id_cidade2)
    distancia = distance.great_circle(c1, c2).km
    return distancia
