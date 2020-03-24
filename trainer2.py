#!/usr/bin/python3

import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


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

# Abre o arquivo que vamos usar para ler os dados
# f = open(path.replace("\n",""))
# path.replace("\n","")

df = pd.read_csv(path.replace("\n",""))
# print(flowMat)

# for i, flow in enumerate(flowMat):
#     if i < 10:
#         print(df.loc[[159220]])
#     else:
#         break
# for i in range(10):
#     print((df.loc[[i]]))

df = df.drop(columns=['Flow ID', ' Source IP', ' Destination IP', ' Timestamp'], axis=1)
labels = np.array(df.iloc[:,-1])
df = df.drop(' Label', axis=1)
df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=1)

traffic = np.array(df)

# print(traffic)

# for i in traffic:
#     print(i)

x_train, x_test, y_train, y_test = train_test_split(traffic, labels, test_size=0.2, random_state=0)
forest_method(x_train, x_test, y_train, y_test)
bayes_method(x_train, x_test, y_train, y_test)
tree_method(x_train, x_test, y_train, y_test)

# print(np.array(labels))
# for i in labels:
#     if i != 'BENIGN':
#         print(i)

    
# cereal_df2 = pd.read_csv("data/cereal.csv")

# Lista contendo as informacoes sobre as colunas
# linha = f.readline().split(',')