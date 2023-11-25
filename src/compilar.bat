@echo off
:: Configuración de la ubicación de dist y build
set DIST_PATH=.\
set WORK_PATH=..\build
set ARCHIVO_PY=renombrar.py

:: Ejecutar pyinstaller con las opciones de configuración
pyinstaller --onefile --distpath=%DIST_PATH% --workpath=%WORK_PATH% %ARCHIVO_PY%

:: Esperar a que el usuario presione una tecla antes de salir
pause

