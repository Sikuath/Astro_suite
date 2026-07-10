@echo off
title Astro Pretraitement

REM Se placer dans le dossier Astro_Pretraitement
cd /d "%~dp0Astro_Pretraitement"

REM Activer le même environnement virtuel
call "..\Astro_Studio\.venv\Scripts\activate.bat"

REM Lancer Streamlit
streamlit run app.py

pause