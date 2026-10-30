@echo off
cd /d "%~dp0"
echo ==========================================
echo Starting Question Paper Generator...
echo ==========================================

if not exist .venv (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing/checking dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Starting Streamlit web application...
python -m streamlit run app.py
pause
