@echo off
echo [1/5] Criando ambiente virtual...
python -m venv venv

echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate

echo [3/5] Atualizando pip e instalando dependências...
pip install --upgrade pip
pip install opencv-python numpy requests

echo [4/5] Baixando modelos Caffe do OpenPose...

if not exist "models" mkdir models
cd models

:: Baixar pose_deploy_linevec.prototxt
echo Baixando prototxt...
curl -L -o pose_deploy_linevec.prototxt https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/body_25/pose_deploy.prototxt

:: Baixar pose_iter_584000.caffemodel
echo Baixando caffemodel...
curl -L -o pose_iter_584000.caffemodel https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/pose/body_25/pose_iter_584000.caffemodel?raw=true

cd ..

echo [5/5] Iniciando o programa...
python main.py

pause
