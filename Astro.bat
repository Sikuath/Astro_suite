@echo off
title Astro Studio

REM Se placer dans le dossier Astro_Studio
cd /d "%~dp0Astro_Studio"

REM Activer l'environnement virtuel
call ".venv\Scripts\activate.bat"

REM Lancer Streamlit
streamlit run app.py

pause