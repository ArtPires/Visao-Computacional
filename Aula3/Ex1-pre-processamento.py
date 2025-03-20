import cv2

# função para mostrar a imagem na tela
def mostraImagem(texto, img):
    cv2.imshow(texto, img)
    cv2.waitKey(0) # aguarda alguma tecla ser pressionada para fechar a imagem
    cv2.destroyAllWindows()

# declaração da imagem utilizada no execício
imagem = cv2.imread("imagens/dog.jpg")
mostraImagem("imagem", imagem)

# Altera o tamanho da imagem para 300px x 300px
img_resize = cv2.resize(imagem, (300, 300))
mostraImagem("imagem-resize", img_resize)

# Rotaciona a imagem com tamanho alterado 49 graus a partir do ponto 200px x 100px
matRot = cv2.getRotationMatrix2D((200,100), 49, 1.0)
imgRot = cv2.warpAffine(img_resize, matRot, img_resize.shape[:2])
mostraImagem("imagem-rotacionada", imgRot)

# Adiciona um desfoque leve na imagem original
imgBlur = cv2.GaussianBlur(imagem, (3, 3), 1)
mostraImagem("imagem-blur", imgBlur)

# Corta a imagem
imgCrop = imagem[0:600, 0:600]
mostraImagem("imagem-crop", imgCrop)