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

    # print("Total de fluxos analisados: %d Erros: %d"% (x_test.shape[0], (y_test != y_pred).sum()))
    print("Acertamos um total de: (bayes)", accuracy_score(y_test, y_pred))


def tree_method(x_train, x_test, y_train, y_test):
    # x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)
    clf = tree.DecisionTreeClassifier()
    y_pred = clf.fit(x_train, y_train).predict(x_test)

    print("Acertamos um total de: (tree)", accuracy_score(y_test, y_pred))

def forest_method(x_train, x_test, y_train, y_test):
    # x_train, x_test, y_train, y_test = train_test_split(matrizTrafego, arrayTipoTrafego, test_size=0.2, random_state=0)
    clf = RandomForestClassifier()
    y_pred = clf.fit(x_train, y_train).predict(x_test)
    
    print("Acertamos um total de: (forest)", accuracy_score(y_test, y_pred))

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

df = df.drop(columns=['Flow ID', ' Source IP', ' Destination IP', ' Timestamp'], axis=1)
labels = np.array(df.iloc[:,-1])
df = df.drop(' Label', axis=1)
df = df.astype(np.float)
df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=1)

traffic = np.array(df)

x_train, x_test, y_train, y_test = train_test_split(traffic, labels, test_size=0.2, random_state=0)
forest_method(x_train, x_test, y_train, y_test)
bayes_method(x_train, x_test, y_train, y_test)
tree_method(x_train, x_test, y_train, y_test)