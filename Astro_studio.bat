@echo off
title Astro Studio

REM Se placer dans le dossier racine Astro_suite
cd /d "%~dp0"

REM Activer l'environnement virtuel commun
call "venv\Scripts\activate.bat"

REM Se placer dans Astro_Studio
cd /d "%~dp0Astro_Studio"

REM Lancer Streamlit avec le venv commun
python -m streamlit run app.py

pause