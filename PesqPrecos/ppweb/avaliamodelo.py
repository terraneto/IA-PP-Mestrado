import numpy as np


def calcula_matriz_de_confusao(reais, preditos, labels):
    """
    Uma função que retorna a matriz de confusão para uma classificação binária

    Args:
        reais (list): lista de valores reais
        preditos (list): lista de valores preditos pelo modelos
        labels (list): lista de labels a serem avaliados.
            É importante que ela esteja presente, pois usaremos ela para entender
            quem é a classe positiva e quem é a classe negativa

    Returns:
        Um numpy.array, no formato:
            numpy.array([
                [ tp, fp ],
                [ fn, tn ]
            ])
    """
    # Erros nos parâmetros
    if len(labels) > 2:
        return None

    if len(reais) != len(preditos):
        return None

    # considerando a primeira classe como a positiva, e a segunda a negativa
    true_class = labels[0]
    negative_class = labels[1]

    # valores preditos corretamente
    tp = 0
    tn = 0

    # valores preditos incorretamente
    fp = 0
    fn = 0

    for (indice, v_real) in enumerate(reais):
        v_predito = preditos[indice]

        # se trata de um valor real da classe positiva
        if v_real == true_class:
            tp += 1 if v_predito == v_real else 0
            fp += 1 if v_predito != v_real else 0
        else:
            tn += 1 if v_predito == v_real else 0
            fn += 1 if v_predito != v_real else 0

    return np.array([
        # valores da classe positiva
        [tp, fp],
        # valores da classe negativa
        [fn, tn]

    ])


def acuracia(mc):
    tp = mc[0, 0]
    tn = mc[1, 1]
    fp = mc[0, 1]
    fn = mc[1, 0]
    acuracia = (tp + tn) / (tp + fp + tn + fn)
    return acuracia


def recall(mc):
    tp = mc[0, 0]
    fn = mc[1, 0]
    return tp / (tp + fn)


def precisao(mc):
    tp = mc[0, 0]
    fp = mc[0, 1]
    return tp / (tp + fp)


def fscore(precisao, recall):
    return 2 * ((precisao * recall) / (precisao + recall))
