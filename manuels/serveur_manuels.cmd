@echo off
REM serveur_manuel_v1.1.cmd — Version 1.1
REM Lance un serveur local pour consulter la documentation HTML
REM Adresse : http://localhost:3501
REM
REM v1.1 : renomme en serveur_manuels : Python en priorite (gere index.html nativement)
REM        node.js en fallback avec URL explicite /index.html
REM v1.0 : creation

setlocal
chcp 65001 >nul

set PORT=3501
set DIR=%~dp0

echo.
echo ============================================================
echo   Documentation Hebreu4.0 — Serveur local port %PORT%
echo   Dossier : %DIR%
echo ============================================================
echo.

REM ── Priorite 1 : Python (virpy13 ou systeme) ──────────────────
set PYTHON=
if exist "C:\virpy13\Scripts\python.exe" (
    set PYTHON=C:\virpy13\Scripts\python.exe
    goto :use_python
)
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON=python
    goto :use_python
)

REM ── Priorite 2 : node.js ──────────────────────────────────────
where npx >nul 2>&1
if %errorlevel% == 0 (
    echo Demarrage via node.js...
    echo Ouvrir : http://localhost:%PORT%/index.html
    echo Ctrl+C pour arreter.
    echo.
    start "" "http://localhost:%PORT%/index.html"
    npx http-server "%DIR%" -p %PORT% --cors -c-1
    goto fin
)

echo ERREUR : ni Python ni node.js trouve.
echo Installez Python (https://python.org) ou Node.js (https://nodejs.org)
pause
goto fin

:use_python
echo Demarrage via Python...
echo Ouvrir : http://localhost:%PORT%/index.html
echo Ctrl+C pour arreter.
echo.
if exist "%DIR%serveur_manuels.py" (
    %PYTHON% "%DIR%serveur_manuels.py" %PORT%
) else (
    REM Fallback ultra-simple : module http.server integre Python
    start "" "http://localhost:%PORT%/index.html"
    cd /d "%DIR%"
    %PYTHON% -m http.server %PORT%
)

:fin
REM serveur_manuel_v1.1.cmd — Version 1.1
