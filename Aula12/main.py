import cv2
from detect_posture import *

proto_path = "models/pose_deploy_linevec_faster_4_stages.prototxt"
model_path = "models/pose_iter_160000.caffemodel"

rede = carregar_rede(proto_path, model_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

print("Pressione 'q' para sair")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    pontos = detectar_pontos(frame, rede)
    frame = desenhar_skeleton(frame, pontos)

    if verifica_bracos_acima(pontos):
        cv2.putText(frame, "Postura: Bracos levantados", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    elif verifica_pernas_afastadas(pontos):
        cv2.putText(frame, "Postura: Pernas afastadas", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    elif verifica_braco_direito_lateral(pontos):
        cv2.putText(frame, "Postura: Braco direito lateral", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Postura: Nao reconhecida", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Deteccao de Postura", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
