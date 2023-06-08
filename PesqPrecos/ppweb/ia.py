import pandas as pd
from sqlalchemy import create_engine
from pyod.models.suod import SUOD
from pyod.models.iforest import IForest
from pyod.models.pca import PCA
from pyod.models.hbos import HBOS
from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.gmm import GMM
from pyod.models.cblof import CBLOF
from pyod.models.lof import LOF
from pyod.models.deep_svdd import DeepSVDD


##################################################################################
# Função recuperar_itens_catmat
# Objetivo: Retornar todos os registros de um determinado material desde uma data
#           especificada até o dia de hoje
# Parâmetros: catmat - código do material a ser recuperado
#             data - Data a partir da qual os registros serão selecionados
# Retorno: dataframe pandas com todos os registros selecionados
##################################################################################
def recuperar_itens_catmat(catmat, data):
    sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df = pd.read_sql(
        'SELECT  quantidade, valor_unitario FROM siasg.itens2 where catmat_id=' + catmat + ' and data>' + data,
        dbConnection);
    return df


##################################################################################
# Função retirar_extremos
# Objetivo: Retirar da base de treinamento os 2,5% maiores valores e os 2,5%
#           menores valores, pela possibilidade de serem erros ou distorções.
#           Não serão retirados mais do que 5% dos registros.
# Parâmetros: df - dataframe pandas com os dados a serem avaliados
# Retorno: dataframe pandas com todos os registros ajustados
##################################################################################
def retirar_extremos(df):
    # calcula o valor unitário onde 97,5% dos registros estão abaixo.
    maior = df['valor_unitario'].quantile(0.975)

    # calcula o valor unitório onde 2,5% dos registros estão abaixo.
    menor = df['valor_unitario'].quantile(0.025)

    # Seleciona todos os registros que estão entre o menor e o maior valor
    dfajustado = df.loc[(df["valor_unitario"] > menor) & (df["valor_unitario"] < maior)]

    # Caso o tamanho do dataframe ajustado seja menor do que 95% dos registros, desconsidera o ajuste
    if len(dfajustado) < (len(df) // (100 / 95)):
        dfajustado = df

    return dfajustado


##################################################################################
# Função treina_modelo
# Objetivo: Treina o modelo de detecção de anomalias
# Parâmetros: df - dataframe pandas com os dados a serem utilizados no treinamento
#             contamination - % estimado de valores anômalos nos dados.
# Retorno: clf - modelo treinado utilizando o SUOD
#          clfdeep - modelo treinado utilizando o DeepSVDD
##################################################################################
def treina_modelo(df, contamination):
    # treina o modelo utilizando o SUOD através da função treina_modelo_suod
    clf = treina_modelo_SUOD(df, contamination)

    # treina o modelo utilizando o DeepSVDD através da função treina_modelo_DeepSVDD
    clfdeep = treina_modelo_DeepSVDD(df, contamination)

    return clf, clfdeep


##################################################################################
# Função treina_modelo_SUOD
# Objetivo: Treina o modelo de detecção de anomalias com a utilização do SUOD
# Parâmetros: df - dataframe pandas com os dados a serem utilizados no treinamento
#             contamination - % estimado de valores anômalos nos dados.
# Retorno: clf - modelo treinado utilizando o SUOD
##################################################################################
def treina_modelo_SUOD(df, contamination):
    # definição de parâmetros que serão utilizados no algoritmo HBOS
    #
    # Por escolha decidiu-se utilizar como 1º parâmetro metade da quantidade de dados
    numerobins = len(df) // 2
    if numerobins < 2: numerobins = 2  # caso seja menos que 2, o número de bins será 2
    #
    # Por escolha decidiu-se utilizar como 2º parâmetro metade do primeiro parâmetro
    nbins2 = numerobins // 2
    if nbins2 < 2: nbins2 = 2  # caso seja menos que 2, o número de bins será 2

    # definição de parâmetros que serão utilizados no algoritmo IFOREST
    #
    # Por escolha decidiu-se utilizar como 1º parâmetro metade da quantidade de dados
    estimadores = len(df) // 2
    if estimadores < 2: estimadores = 2  # caso seja menos que 2, o número será 2
    # Por escolha decidiu-se utilizar como 2º parâmetro 1/5 da quantidade do primeiro
    estimadores2 = estimadores // 5
    if estimadores2 < 2: estimadores2 = 2  # caso seja menos que 2, o número será 2

    # definição de parâmetros que serão utilizados no algoritmo LOF
    #
    # Por escolha decidiu-se utilizar como 1º parâmetro 6% da quantidade de dados
    numero_vizinhos = int(round(len(df) * 0.06, 0))

    contamination2 = contamination + 0.03
    # Lista de detectores
    detector_list = [HBOS(n_bins=numerobins, alpha=contamination, contamination=contamination),
                     HBOS(n_bins=nbins2, alpha=contamination, contamination=contamination),
                     ECOD(contamination=contamination),
                     COPOD(contamination=contamination),
                     GMM(contamination=contamination),
                     PCA(n_components=2, n_selected_components=2, contamination=contamination),
                     PCA(n_components=2, n_selected_components=1, contamination=contamination),
                     IForest(n_estimators=estimadores, contamination=contamination),
                     IForest(n_estimators=estimadores2, contamination=contamination),
                     CBLOF(contamination=contamination),
                     LOF(n_neighbors=numero_vizinhos, contamination=contamination)
                     ]

    clf = SUOD(base_estimators=detector_list, n_jobs=2, combination='maximization', contamination=contamination,
               verbose=False)
    clf.fit(df)
    return clf


def treina_modelo_DeepSVDD(df, contamination):
    clfdeep = DeepSVDD(verbose=0, preprocessing=True, contamination=contamination)
    clfdeep.fit(df)
    return clfdeep


def avalia_dados(clf, clfdeep, quantidade, valor):
    dfteste = pd.DataFrame({'quantidade': quantidade, 'valor_unitario': valor}, index=[0])
    clf.predict(dfteste, return_confidence=False)
    clfdeep.predict(dfteste, return_confidence=False)
    predicao = clf.predict(dfteste) + clfdeep.predict(dfteste)
    predicao[predicao > 1] = 1
    return predicao


def avalia_dados_dataframe(clf, clfdeep, df):
    clf.predict(df, return_confidence=False)
    clfdeep.predict(df, return_confidence=False)
    predicao = clf.predict(df) + clfdeep.predict(df)
    predicao[predicao > 1] = 1
    return predicao
