import cv2
import math

def carregar_rede(proto_path, model_path):
    return cv2.dnn.readNetFromCaffe(proto_path, model_path)

def detectar_pontos(imagem, network, numero_pontos=15, threshold=0.1):
    blob = cv2.dnn.blobFromImage(image=imagem, scalefactor=1.0/255, size=(imagem.shape[1], imagem.shape[0]))
    network.setInput(blob)
    output = network.forward()
    pontos = []

    altura, largura = output.shape[2], output.shape[3]

    for i in range(numero_pontos):
        mapa_confianca = output[0, i, :, :]
        _, confianca, _, ponto = cv2.minMaxLoc(mapa_confianca)
        x = int((imagem.shape[1] * ponto[0]) / largura)
        y = int((imagem.shape[0] * ponto[1]) / altura)
        pontos.append((x, y) if confianca > threshold else None)

    return pontos

def verifica_bracos_acima(pontos):
    if pontos[0] and pontos[4] and pontos[7]:
        return pontos[4][1] < pontos[0][1] and pontos[7][1] < pontos[0][1]
    return False

def verifica_pernas_afastadas(pontos):
    if pontos[8] and pontos[11] and pontos[10] and pontos[13]:
        return pontos[13][0] > pontos[11][0] and pontos[10][0] < pontos[8][0]
    return False

def verifica_braco_direito_lateral(pontos):
    if pontos[2] and pontos[3] and pontos[4]:
        ombro = pontos[2]
        cotovelo = pontos[3]
        pulso = pontos[4]

        delta_x = abs(pulso[0] - ombro[0])
        delta_y = abs(pulso[1] - ombro[1])

        return delta_x > 100 and delta_y < 30
    return False

def desenhar_skeleton(imagem, pontos):
    conexoes = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14],
                [14,8], [8,9], [9,10], [14,11], [11,12], [12,13]]

    for a, b in conexoes:
        if pontos[a] and pontos[b]:
            cv2.line(imagem, pontos[a], pontos[b], (255, 0, 0), 2)
            cv2.circle(imagem, pontos[a], 3, (0, 255, 0), -1)
            cv2.circle(imagem, pontos[b], 3, (0, 255, 0), -1)

    return imagem

