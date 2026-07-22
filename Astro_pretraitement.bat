@echo off
title Astro Pretraitement

REM Racine Astro_suite
set ROOT=%~dp0

REM Aller dans le module
cd /d "%ROOT%Astro_Pretraitement"

REM Lancer avec le Python du venv commun
"%ROOT%.venv\Scripts\python.exe" -m streamlit run app.py

pause