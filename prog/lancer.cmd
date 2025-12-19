@echo off
REM Début de "lancer.cmd" version "2.2"
cls
echo.
echo lancer.cmd — Version 2.2
echo.

:: Activation de l'environnement virtuel si nécessaire
where python | findstr /i "virPy13" >nul
if %errorlevel% neq 0 (
    echo Activation de l'environnement virtuel virPy13...
    call C:\virPy13\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo [ERREUR] Impossible d'activer virPy13
        pause
        exit /b 1
    )
)

:: Aller dans le répertoire du projet
cd /d "%~dp0\.."

echo.
echo === Génération du site réel à partir du dossier documents ===

:: 1. On lance d'abord genere_site.py (il crée html/ et tous les dossiers)
python prog\genere_site.py
if %errorlevel% neq 0 (
    echo [ERREUR] genere_site.py a échoué
    pause
    exit /b 1
)

:: 2. Ensuite seulement on génère la TDM (html/ existe maintenant → plus d'erreur)
python prog\cree_table_des_matieres.py
if %errorlevel% neq 0 (
    echo [ERREUR] cree_table_des_matieres.py a échoué
    pause
    exit /b 1
)
rem créer /Hebreu4.0/html/Hebreu4.0/html/style.css
xcopy html\style.css html\Hebreu4.0\html\style.css

echo.
echo === Démarrage du serveur local ===
npx http-server html -p 3500 --cors -c-1 -o "/index.html"

echo.
echo Site réel disponible sur : http://localhost:3500/index.html
echo.
pause
REM Fin de "lancer.cmd" version "2.2"