from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import base64
import numpy as np

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
        return render_template('index.html', mensagem="Nenhum arquivo enviado")

    file = request.files['imagem']
    if file.filename == '':
        return render_template('index.html', mensagem="Nome de arquivo inválido")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    processed_img_base64 = process_image(file_path)

    return render_template('index.html', mensagem="Imagem processada!", imagem=processed_img_base64)

def process_image(image_path):
    img = cv2.imread(image_path)
    img = convert_image(img)
    img = apply_blur(img)

    _, buffer = cv2.imencode('.png', img)  # Codifica a imagem em PNG
    img_base64 = base64.b64encode(buffer).decode('utf-8')  # Converte para string base64
    return f"data:image/png;base64,{img_base64}"  # Retorna a string para o HTML


def convert_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

def apply_blur(image):
    return cv2.blur(image[:,:,0],(15,15),0)

if __name__ == '__main__':
    app.run(debug=True)
