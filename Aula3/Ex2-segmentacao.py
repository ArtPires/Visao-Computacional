import cv2

# função para mostrar a imagem na tela
def mostraImagem(texto, img):
    cv2.imshow(texto, img)
    cv2.waitKey(0) # aguarda alguma tecla ser pressionada para fechar a imagem
    cv2.destroyAllWindows()

# Declara a imagem na escala de cinza
imagem = cv2.imread("imagens/book.jpg", 0)

# Aplica um desfoque para remover o ruído da imagem original
imgBlur = cv2.GaussianBlur(imagem, (3, 3), 1)

# Aplica o threshold binário na imagem
ret, thresh1 = cv2.threshold(imagem, 117, 255, cv2.THRESH_BINARY)
mostraImagem("threshold binario", thresh1)

# Aplica o threshold adaptativo na imagem
thresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
mostraImagem("threshold adaptativo", thresh)