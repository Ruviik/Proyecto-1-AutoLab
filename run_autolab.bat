@echo off
:: Forzar codificación UTF-8 para ver emojis
chcp 65001 >nul

TITLE AutoLab Launcher
CLS

:: Forzar directorio actual
cd /d "%~dp0"

ECHO ==========================================
ECHO      🚀 INICIANDO AUTOLAB v2.0
ECHO ==========================================

:: 1. Comprobar Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ❌ ERROR: Python no encontrado.
    ECHO Asegurate de tener Python instalado y en el PATH.
    PAUSE
    EXIT
)

:: 2. Comprobar entorno virtual
IF EXIST "venv" (
    ECHO ✅ Entorno virtual detectado.
) ELSE (
    ECHO 📦 Creando entorno virtual...
    python -m venv venv
)

:: 3. Activar entorno
IF NOT EXIST "venv\Scripts\activate.bat" (
    ECHO ❌ ERROR: No encuentro el script de activacion.
    ECHO Borra la carpeta 'venv' y vuelve a ejecutar este archivo.
    PAUSE
    EXIT
)

call venv\Scripts\activate.bat

:: 4. Instalar librerias (solo si hace falta)
IF EXIST "requirements.txt" (
    ECHO ⬇️  Verificando dependencias...
    pip install -r requirements.txt >nul 2>&1
)

:: 5. Ejecutar APP
ECHO.
ECHO ✅ Todo listo. Lanzando aplicacion...
ECHO ------------------------------------------
python src/main.py

:: 6. Pausa final para ver errores si los hay
ECHO.
ECHO ==========================================
ECHO 🏁 Ejecucion finalizada.
PAUSE