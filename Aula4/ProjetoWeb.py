from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files['imagem']
    if file.filename == '':
        return "Nome de arquivo inválido", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    showImage(file_path)

    return f"Imagem salva em {file_path}", 200

def showImage(imagem):
    img = cv2.imread(imagem)
    convertImage(img)
    blur_img = applyBlur(img)

    cv2.imshow("imagem", blur_img)
    cv2.waitKey(0)  # aguarda alguma tecla ser pressionada para fechar a imagem
    cv2.destroyAllWindows()

def convertImage(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

def applyBlur(image):
    return cv2.blur(image[:,:,0],(15,15),0)

if __name__ == '__main__':
    app.run(debug=True)
