import pandas as pd
from sqlalchemy import create_engine


###################################################################
# Função recuperar_itens_catmat
# Objetivo: Retornar todos os registros de um determinado material
#           desde uma data especificada até o dia de hoje
# Parâmetros: catmat - código do material a ser recuperado
#             data - Data a partir da qual os registros serão
#                    selecionados
# Retorno: dataframe pandas com todos os registros selecionados
###################################################################
def recuperar_itens_catmat(catmat, data):
    # Cria a conexão com o servidor de banco de dados
    sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
    dbConnection = sqlEngine.connect()

    # Lê o banco de dados para buscar os registros que atendem os parametros informados
    df = pd.read_sql(
        "SELECT  quantidade, valor_unitario, distancia_uasg_fornecedor  FROM siasg.itens where catmat_id=" + str(
            catmat) + " and data > '" + data
        + "'", dbConnection)
    return df


###################################################################
# Função recuperar_licitacoes_contratos_catmat
# Objetivo: Retornar as licitações e contratos de um determinado
#            material desde uma data especificada até o dia de hoje
# Parâmetros: catmat - código do material a ser recuperado
#             data - Data a partir da qual os registros serão
#                    selecionados
# Retorno: dataframe pandas com todos os registros selecionados
###################################################################
def recuperar_licitacoes_contratos_catmat(catmat, data):
    # Cria a conexão com o servidor de banco de dados
    sqlEngine = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
    dbConnection = sqlEngine.connect()

    # Lê o banco de dados para buscar os registros que atendem os parametros informados
    df = pd.read_sql(
        "SELECT  *  FROM siasg.itenscompletos where catmat_id=" + str(
            catmat) + " and data > '" + data
        + "'", dbConnection)
    return df


#########################################################################
# Função preprocessar_dados
# Objetivo: Realizar o pré-processamento dos dados
# Parametros: df - dataframe pandas com os dados a serem escalonados
# Retorno: dataframe pandas com todos os registros ajustados utilizando
#          o método Robust de escalonamento
#########################################################################
from sklearn.preprocessing import RobustScaler


def preprocessar_dados(df):
    # Cria uma instância do RobustScaler
    robust_scaler = RobustScaler()

    # Ajusta e transforma os dados com o RobustScaler
    df_ajustado = robust_scaler.fit_transform(df)

    # retorna o dataframe ajustado
    return df_ajustado


##################################################################################
# Função treina_modelo
# Objetivo: Treina o modelo de detecção de anomalias
# Parâmetros: df - dataframe pandas com os dados a serem utilizados no treinamento
#             contamination - % estimado de valores anômalos nos dados.
# Retorno: clf - modelo treinado utilizando o SUOD
#          clfdeep - modelo treinado utilizando o DeepSVDD
##################################################################################
def treina_modelo(df, contamination):
    # treina o modelo
    clf = COPOD(contamination=contamination)
    clf.fit(df)
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


#####################################################
# Funcao treina_modelo_inicial
# Objetivo: Treina o modelo de detecção de anomalias
# Parâmetros: df - dataframe pandas com  os  dados a
#                  serem utilizados no treinamento
# Retorno: clf - modelo treinado utilizando o SUOD
#####################################################
# Importa bibliotecas do PyOD com os algoritmos de detecção de anomalias
from pyod.models.inne import INNE
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.pca import PCA
from pyod.models.sampling import Sampling
from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.suod import SUOD


def treina_modelo_inicial(df):
    # Lista de detectores
    detector_list = [
        INNE(contamination=0.05, n_estimators=50, random_state=69),
        KNN(contamination=0.05, leaf_size=10, method='largest', n_neighbors=10),
        LOF(contamination=0.05, leaf_size=1, n_neighbors=34),
        PCA(contamination=0.05, n_components=3, n_selected_components=1),
        Sampling(contamination=0.05, subset_size=10),
        ECOD(contamination=0.09),
        COPOD(contamination=0.12)
    ]

    # configurar o SUOD com a lista de parâmetros e detectores
    clf = SUOD(base_estimators=detector_list, n_jobs=2, combination='maximization', contamination=0.05,
               verbose=False)

    # treinar o modelo
    clf.fit(df)
    return clf


def avalia_dados(clf, quantidade, valor, distancia):
    dfteste = pd.DataFrame({'quantidade': quantidade, 'valor_unitario': valor, 'distancia': distancia}, index=[0])
    predicao = clf.predict(dfteste)
    return predicao


def avalia_dados_dataframe(clf, df):
    predicao = clf.predict(df)
    return predicao
