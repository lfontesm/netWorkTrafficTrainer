#!/usr/bin/python3

import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def traffic_to_f(string):
    if string == 'BENIGN':
        return 1.0
    else:
        return 0.0

# valor default quando chega no final do arquivo
def default():
    trafego = np.array(["0"]).astype(np.float)
    tipoTrafego = -1
    checkErr = 1

    return trafego, tipoTrafego, checkErr
        

# Funcao que sera wrapeada pela selec_prox_a
def _selec_prox_a(file):
    linha = file.readline()
    if not linha:
        return default()

    linha = linha.split(',')
    linha = [i.strip() for i in linha]
    
    tipoTrafego = linha.pop(-1)
    tipoTrafego = traffic_to_f(tipoTrafego)            # Remove a classificacao do trafego e transforma ele em um numero que possa ser treinado
    
    linha = np.array(linha)

    trafego = np.delete(linha, np.s_[0:2])             # Tira campos que nao serao usados
    trafego = np.delete(trafego, 1)
    trafego = np.delete(trafego, 3)

    trafego = trafego.astype(np.float)                 # Transforma em um array de reais

    return (trafego, tipoTrafego, 0)

# Seleciona o proximo array que sera incorporado na matriz de trafego, descartando resultados com valores inaceitaveis
def selec_prox_a(file):
    trafego, tipoTrafego, err = _selec_prox_a(file)
    while err != 1 and (np.any(np.isinf(trafego)) or np.any(np.isnan(trafego))):  # Checa para ver se algum dos valores do array lido eh nao-aceitavel
        trafego, tipoTrafego, err = _selec_prox_a(file)                           # (NaN ou inf)
    
    if err == 1:
        return default()

    return (trafego, tipoTrafego, 0)

def cria_matrizTrafego(file):
    (matrizTrafego, tipoTrafego, err) = selec_prox_a(file)
    if err == 1:
        return
    matrizTrafego = np.matrix(matrizTrafego)
    arrayTipoTrafego = []
    arrayTipoTrafego.append(tipoTrafego)
    
    i = 0
    maxIt = 1000000   # Ajuste esse numero para mudar o numero de linhas lido no arquivo de entrada
    while True:       # 1.000.000 deve ser o suficiente para ler qualquer arquivo.
        arrayTrafego, tipoTrafego, err = selec_prox_a(file)
        if err == 1 or i >= maxIt:
            break
        matrizTrafego = np.append(matrizTrafego, np.matrix(arrayTrafego), axis=0)
        arrayTipoTrafego.append(tipoTrafego)
        i = i+1

    return matrizTrafego, arrayTipoTrafego

def bayes_method(x_train, x_test, y_train, y_test):
    # x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)
    gnb = GaussianNB()
    y_pred = gnb.fit(x_train, y_train).predict(x_test)

    print("Total de fluxos analisados: %d Erros: %d"% (x_test.shape[0], (y_test != y_pred).sum()))

def tree_method(x_train, x_test, y_train, y_test):
    # x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)
    clf = tree.DecisionTreeClassifier()
    y_pred = clf.fit(x_train, y_train).predict(x_test)

    print("Acertamos um total de: ", accuracy_score(y_test, y_pred))

def forest_method(x_train, x_test, y_train, y_test):
    # x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)
    clf = RandomForestClassifier()
    y_pred = clf.fit(x_train, y_train).predict(x_test)
    
    print("Acertamos um total de: ", accuracy_score(y_test, y_pred))
    


# Pega o caminho do arquivo que vamos abrir
# ex: TrafficLabelling/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
pathFile = open('path')
path = pathFile.readline()
print(path)
# print(type(path))

# Abre o arquivo que vamos usar para ler os dados
f = open(path.replace("\n",""))

# Lista contendo as informacoes sobre as colunas
linha = f.readline().split(',')

matrizTrafego, arrayTipoTrafego = cria_matrizTrafego(f)

# Separa entre os vetores de treinamento e de teste
x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)

# bayes_method(x_train, x_test, y_train, y_test)
# bayes_method(matrizTrafego, arrayTipoTrafego)
tree_method(x_train, x_test, y_train, y_test)
# forest_method(x_train, x_test, y_train, y_test)

# a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
# b = np.array([1, 2, 3, 5, 5, 6, 7, 8, 9])
# print((a != b).sum())

# x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.3, random_state=0)
# gnb = GaussianNB()

# y_pred = gnb.fit(x_train, y_train).predict(x_test)

# print("Total de fluxos analisados: %d Erros: %d"% (x_test.shape[0], (y_test != y_pred).sum()))