import pandas as pd
from pyod.models.ecod import ECOD
from pyod.models.lof import LOF
from pyod.models.pca import PCA
from pyod.models.suod import SUOD
from sqlalchemy import create_engine


###################################################################
# Funcao recuperar_itens_catmat
# Objetivo: Retornar todos os registros de um determinado material
#           desde uma data especificada ate o dia de hoje
# Parametros: catmat - codigo do material a ser recuperado
#             data - Data a partir da qual os registros serao
#                    selecionados
# Retorno: dataframe pandas com todos os registros selecionados
###################################################################
def recuperar_itens_catmat(catmat, data):
    # Cria a conexao com o servidor de banco de dados
    sqlengine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
    dbconnection = sqlengine.raw_connection()

    # Le o banco de dados para buscar os registros que atendem os parametros informados
    df = pd.read_sql(
        "SELECT  quantidade, valor_unitario FROM siasg.itens2 where catmat_id=" + str(catmat) + " and data > '" + data
        + "'", dbconnection)
    return df


###################################################################
# Funcao retirar_extremos
# Objetivo: Retirar da base de treinamento os 2,5% maiores valores
#           e os 2,5% menores valores, pela possibilidade de serem
#           erros ou distorções. Não serão retirados  mais  do que
#           5% dos registros.
# Parametros: df - dataframe pandas com os dados a serem avaliados
# Retorno: dataframe pandas com todos os registros ajustados
###################################################################
def retirar_extremos(df):
    # calcula o valor unitario onde 97,5% dos registros estao abaixo.
    maior = df['valor_unitario'].quantile(0.975)

    # calcula o valor unitario onde 2,5% dos registros estao abaixo.
    menor = df['valor_unitario'].quantile(0.025)

    # Seleciona todos os registros que estao entre o menor e o maior valor
    dfajustado = df.loc[(df["valor_unitario"] > menor) & (df["valor_unitario"] < maior)]

    # Caso o tamanho do dataframe ajustado seja menor do que 95% dos registros, desconsidera o ajuste
    if len(dfajustado) < (len(df) // (100 / 95)):
        dfajustado = df

    # retorna o dataframe ajustado
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
    clf = treina_modelo_suod(df, contamination)
    return clf


##################################################################################
# Função treina_modelo_SUOD
# Objetivo: Treina o modelo de detecção de anomalias com a utilização do SUOD
# Parâmetros: df - dataframe pandas com os dados a serem utilizados no treinamento
#             contamination - % estimado de valores anômalos nos dados.
# Retorno: clf - modelo treinado utilizando o SUOD
##################################################################################
def treina_modelo_suod(df, contamination):
    # definição de parâmetros que serão utilizados no algoritmo HBOS
    try:
        # Lista de detectores
        detector_list = [ECOD(contamination=contamination),
                         PCA(n_components=2, n_selected_components=1, contamination=contamination),
                         LOF(n_neighbors=21, contamination=contamination)
                         ]
        clf = SUOD(base_estimators=detector_list, n_jobs=2, combination='average',
                   verbose=False)
        clf.fit(df)
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
    return clf


def avalia_dados(clf, quantidade, valor):
    dfteste = pd.DataFrame({'quantidade': quantidade, 'valor_unitario': valor}, index=[0])
    predicao = clf.predict(dfteste)
    return predicao


def avalia_dados_dataframe(clf, df):
    predicao = clf.predict(df)
    return predicao
