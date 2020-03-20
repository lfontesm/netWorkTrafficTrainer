#!/usr/bin/python3

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

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
    while err != -1 and (np.any(np.isinf(trafego)) or np.any(np.isnan(trafego))): # Checa para ver se algum dos valores do array lido eh nao-aceitavel
        trafego, tipoTrafego, err = _selec_prox_a(file)                           # (NaN ou inf)
    
    # print(trafego)
    # print(tipoTrafego)
    if err == 1:
        return default()

    return (trafego, tipoTrafego, 0)

def cria_matrizTrafego(file):
    (matrizTrafego, tipoTrafego, err) = selec_prox_a(file)
    if err == 1:
        return
    matrizTrafego = np.matrix(matrizTrafego)
    arrayTipoTrafego = []
    # print(tipoTrafego)
    arrayTipoTrafego.append(tipoTrafego)
    
    # print(matrizTrafego)
    # print(arrayTipoTrafego[0])
    # print(type(arrayTipoTrafego))
    # return
    
    i = 0
    maxIt = 5000
    while True:
        arrayTrafego, tipoTrafego, err = selec_prox_a(file)
        if err == 1 or i >= maxIt:
            break
        # print(matrizTrafego)
        # print(np.matrix(arrayTrafego))
        matrizTrafego = np.append(matrizTrafego, np.matrix(arrayTrafego), axis=0)
        arrayTipoTrafego.append(tipoTrafego)
        i = i+1

    # print(matrizTrafego)
    # print(arrayTipoTrafego)

    return matrizTrafego, arrayTipoTrafego
    
    # arrayTipoTrafego = np.append()
    # i = 0
    # maxIt = 10
    # for linha in file:
    #     if i < maxIt:
    #         arrayTrafego = selec_prox_a(linha)



    # matrizTrafego = np.append(np.matrix(matrizTrafego))
    

    # print(matrizTrafego)
    # print(classificacoes)
    
    
    
    
    
    
    
    

# def cria_matrizTrafego(file):
#     matrizTrafego = file.readline().split(',')                             # Le a primeira linha e guarda 
#     matrizTrafego = [i.strip() for i in matrizTrafego]                     # em uma variavel do tipo np.matrix.
#     matrizTrafego = np.matrix(matrizTrafego)                               # Onde sera usada para guardar o restante do arquivo
#     i = 0
#     linhasMax = 1
#     for linha in file:
#         # Comente essa linha e tire a indentacao para ler e treinar a matriz completa
#         if i < linhasMax:
#             linha = linha.split(',')
#             linha = [i.strip() for i in linha]
#             classPos = len(linha)-1
#             classificacoes = arrayTrafego[:,classPos] 
#             arrayTrafego = np.matrix(linha)
#             arrayTrafego = np.delete(arrayTrafego, np.s_[0:2], axis=1) # Remove as colunas que nao vamos usar
#             arrayTrafego = np.delete(arrayTrafego, 1, axis=1)
#             arrayTrafego = np.delete(arrayTrafego, 3, axis=1)          
                            
#             classificacoes = arrayTrafego[:,classPos]          
#             print(classPos) 
#             # arrayTrafego = arrayTrafego.astype(np.float)

#             # temp = np.array(matrizTrafego)              # Variavel temporaria soh para nao precisar escrever "classificacoes" mtas vezes

#             print(arrayTrafego)
#             if np.all(np.isfinite(arrayTrafego)):
#                 continue
#             matrizTrafego = np.append(matrizTrafego, arrayTrafego, axis=0) # Comeca a guardar linha por linha na matrix de trafego


#             i = i + 1

#     return matrizTrafego   

# Pega o caminho do arquivo que vamos abrir
# Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
pathFile = open('path')
path = pathFile.readline()
print(path)
# print(type(path))

# Abre o arquivo que vamos usar para ler os dados
f = open(path.replace("\n",""))

# Lista contendo as informacoes sobre as colunas
linha = f.readline().split(',')
# nomeColunas = [i.strip() for i in linha] # Nao sera usado

matrizTrafego, arrayTipoTrafego = cria_matrizTrafego(f)
# matrizTrafego = np.delete(matrizTrafego, np.s_[0:2], axis=1) # Remove as colunas que nao vamos usar
# matrizTrafego = np.delete(matrizTrafego, 1, axis=1)
# matrizTrafego = np.delete(matrizTrafego, 3, axis=1)          

# print(matrizTrafego[0],"\n\n\n")
for i in matrizTrafego:
    print(i,"\n")

print(arrayTipoTrafego)
# temp = np.array(matrizTrafego)              # Variavel temporaria soh para nao precisar escrever "classificacoes" mtas vezes
# classPos = len(temp[0])-1                   # Posicao da classificacao nas matrizes
# classificacoes = temp[:,classPos]           # Separa a ultima coluna, que representa a classificacao correta do trafego em uma lista
# print(classificacoes,"\n\n\n")

# Retira a ultima coluna da matriz de trafego
# _matrizTrafego = np.delete(matrizTrafego, classPos, 1)
# _matrizTrafego = np.array(_matrizTrafego)#.astype(np.float)
# print(_matrizTrafego[0])
# a = 0
# for i in _matrizTrafego:
#     print("Linha: ", a)
#     print(i,"\n\n")
#     a=a+1



# print(np.any(np.isnan(_matrizTrafego)))
# print(np.all(np.isfinite(_matrizTrafego)))

# x_train, x_test, y_train, y_test = train_test_split(_matrizTrafego, classificacoes, test_size=0.3, random_state=0)
# gnb = GaussianNB()

# y_pred = gnb.fit(x_train, y_train).predict(x_test)

# print("Total de fluxos analisados: %d Erros: %d"% (x_test.shape[0], (y_test != y_pred).sum()))


# for i in _matrizTrafego:
    # print(i,"\n")

# t = le_linha(f)
# print(t)

# mat = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
# ]

# l1 = [1, 2, 3, 4]
# l2 = [5, 6, 7, 8]

# l1 = np.matrix(l1)
# l1 = np.append(l1, np.matrix(l2), axis=0)
# # l1 = np.append(l1, l2, axis=1)

# for i in l1:
#     print(np.array(i),"\n")

# c = separa_classificacao(mat)

# print(len(c))
 