from flask import Flask, render_template, request, session
import cv2
import os
import base64
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'segredo-do-pitao'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'imagem' not in request.files:
            return render_template('index.html', mensagem="Nenhum arquivo enviado")

        file = request.files['imagem']
        if file.filename == '':
            return render_template('index.html', mensagem="Nome de arquivo inválido")

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        session['imagem_path'] = file_path

        with open(file_path, "rb") as f:
            img_bytes = f.read()
            imagem_original_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return render_template(
            'index.html',
            mensagem="Imagem enviada!",
            imagem_original=f"data:image/png;base64,{imagem_original_base64}",
            efeito_selecionado='original'
        )

    return render_template('index.html')


@app.route('/efeito', methods=['POST'])
def aplicar_efeito():
    efeito = request.form.get('efeito')
    imagem_path = session.get('imagem_path')

    if not imagem_path or not os.path.exists(imagem_path):
        return render_template('index.html', mensagem="Nenhuma imagem enviada!")

    imagem_processada_base64 = process_image(imagem_path, efeito)

    with open(imagem_path, "rb") as f:
        original_bytes = f.read()
        imagem_original_base64 = base64.b64encode(original_bytes).decode('utf-8')

    return render_template(
        'index.html',
        mensagem=f"Efeito '{efeito}' aplicado!",
        imagem_original=f"data:image/png;base64,{imagem_original_base64}",
        imagem_processada=imagem_processada_base64,
        efeito_selecionado=efeito
    )


def process_image(image_path, efeito):
    imagem = cv2.imread(image_path)

    if efeito == 'resize':
        imagem = cv2.resize(imagem, (300, 300), interpolation=cv2.INTER_LINEAR)

    elif efeito == 'rotacionar':
        height, width = imagem.shape[:2]
        matRot = cv2.getRotationMatrix2D((width // 2, height // 2), 49, 1.0)
        imagem = cv2.warpAffine(imagem, matRot, (width, height))

    elif efeito == 'blur':
        imagem = cv2.GaussianBlur(imagem, (21, 21), 5)

    elif efeito == 'threshold_bin':
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        _, imagem = cv2.threshold(gray, 117, 255, cv2.THRESH_BINARY)

    elif efeito == 'threshold_adapt':
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        imagem = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

    elif efeito == 'erosao':
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5, 5), np.uint8)
        imagem = cv2.erode(gray, kernel, iterations=1)

    elif efeito == 'dilatacao':
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5, 5), np.uint8)
        imagem = cv2.dilate(gray, kernel, iterations=1)

    _, buffer = cv2.imencode('.png', imagem)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


if __name__ == '__main__':
    app.run(debug=True)
