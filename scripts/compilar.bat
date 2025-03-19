@echo off
chcp 65001 > nul
title Compilador de Renombrar Fotos

:menu
cls
echo ============================================
echo    Compilador de Renombrar Fotos
echo ============================================
echo.
echo 1. Registrar en menú contextual (requiere admin)
echo 2. Crear ejecutable .exe
echo 3. Instalar paquete en modo desarrollo
echo 4. Salir
echo.
echo ============================================
echo.

set /p opcion="Seleccione una opción (1-4): "

if "%opcion%"=="1" goto registrar
if "%opcion%"=="2" goto crear_exe
if "%opcion%"=="3" goto instalar
if "%opcion%"=="4" goto salir
goto menu

:registrar
cls
echo Registrando en menú contextual...
python registrar_menu_contextual.py
echo.
echo Presione cualquier tecla para volver al menú...
pause > nul
goto menu

:crear_exe
cls
echo Creando ejecutable...
python crear_ejecutable.py
echo.
echo Presione cualquier tecla para volver al menú...
pause > nul
goto menu

:instalar
cls
echo Instalando paquete en modo desarrollo...
cd ..
pip install -e .
cd scripts
echo.
echo Presione cualquier tecla para volver al menú...
pause > nul
goto menu

:salir
cls
echo Gracias por usar el compilador!
timeout /t 2 > nul
exit 