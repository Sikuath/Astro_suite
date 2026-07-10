@echo off
title Astro Pretraitement

REM Se placer dans le dossier racine Astro_suite
cd /d "%~dp0"

REM Activer l'environnement virtuel commun
call "venv\Scripts\activate.bat"

REM Se placer dans Astro_Pretraitement
cd /d "%~dp0Astro_Pretraitement"

REM Lancer Streamlit avec le Python du venv
python -m streamlit run app.py

pause