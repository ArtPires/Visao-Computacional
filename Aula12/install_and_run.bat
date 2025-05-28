@echo off
echo ===============================
echo  Criando ambiente virtual...
echo ===============================
python -m venv venv

echo ===============================
echo  Ativando ambiente virtual...
echo ===============================
call venv\Scripts\activate.bat

echo ===============================
echo  Atualizando pip...
echo ===============================
python -m pip install --upgrade pip

echo ===============================
echo  Instalando dependências...
echo ===============================
pip install -r requirements.txt

echo ===============================
echo  Iniciando o programa...
echo ===============================
python main.py

echo ===============================
echo  Encerrado.
echo ===============================
pause
