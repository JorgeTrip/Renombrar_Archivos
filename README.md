# Renombrar Archivos de Fotos y Videos - v1.9.0

[![Descargar para Windows](https://img.shields.io/badge/Descargar-Windows_.exe-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/JorgeTrip/Renombrar_Archivos/releases/latest/download/RenombrarFotos.exe)
[![Última Versión](https://img.shields.io/github/v/release/JorgeTrip/Renombrar_Archivos?style=for-the-badge&color=success)](https://github.com/JorgeTrip/Renombrar_Archivos/releases/latest)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)](LICENSE)

Una herramienta profesional en Python para renombrar automáticamente archivos de fotos y videos, agregando la fecha y hora al inicio del nombre para optimizar la organización cronológica. Soporta tanto análisis por patrones de nombres como extracción de metadatos incrustados (EXIF / Video).

## 📥 Descarga Rápida (Ejecutable para Windows)

No necesitas tener Python instalado. Puedes descargar directamente el archivo ejecutable listo para usar:

👉 **[Descargar RenombrarFotos.exe (Última versión)](https://github.com/JorgeTrip/Renombrar_Archivos/releases/latest/download/RenombrarFotos.exe)**

> Para ver las notas de cada versión y versiones anteriores, visita la sección de [Releases de GitHub](https://github.com/JorgeTrip/Renombrar_Archivos/releases).

## Características Principales

### 🖥️ Interfaz de Usuario Mejorada
- **Selector de Criterio**: Elige entre búsqueda por patrones en el nombre o metadatos incrustados.
- **Pantalla de Bienvenida y Título Centrado**: Presentación profesional adaptada al ancho del terminal.
- **Confirmación Interactiva**: Avisos detallados para archivos sin metadatos o sin información de hora.

### 📁 Gestión Inteligente de Archivos
- **Búsqueda Recursiva**: Analiza el directorio actual y todos sus subdirectorios.
- **Selección Flexible**: Elige carpetas específicas o procesa todo en bloque.
- **Prevención de Colisiones**: Maneja archivos duplicados agregando sufijos alfabéticos.

### 🔄 Transformaciones de Nombres
- **Archivos de Imagen (IMG)**: `IMG_20230315_143022.jpg` → `2023-03-15 14-30-22 - IMG_20230315_143022.jpg`
- **Archivos de Teléfono**: `20231225_090000.mp4` → `2023-12-25 09-00-00 - 20231225_090000.mp4`
- **Archivos de Video (VID)**: `VID_20240101_120000.mkv` → `2024-01-01 12-00-00 - VID_20240101_120000.mkv`
- **Por Metadatos**: Extrae fecha y hora real de captura desde EXIF / contenedores multimedia.

### 🎯 Formatos Soportados
- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`, `.webp`, `.tiff`
- **Videos**: `.mp4`, `.mkv`, `.mov`, `.avi`, `.wmv`, `.flv`, `.webm`, `.m4v`

## Requisitos e Instalación

- Python 3.8 o superior (Windows, Linux, macOS)

```bash
git clone https://github.com/JorgeTrip/Renombrar_Archivos.git
cd Renombrar_Archivos
pip install -r requirements.txt
```

## Formas de Uso

### 1. Como Script de Python
Ejecuta directamente desde el directorio del proyecto:
```bash
python renombrarfotos.py
```

### 2. Como Ejecutable Independiente (PyInstaller)
```bash
python scripts/crear_ejecutable.py
# o bien
python -m PyInstaller scripts/RenombrarFotos.spec --clean
```
El ejecutable se genera en `dist/RenombrarFotos.exe`.

### 3. Como Paquete Instalado
```bash
pip install -e .
renombrar
```

## Flujo de Trabajo
1. **Bienvenida**: Muestra ejemplos y confirma inicio.
2. **Selector de Criterio**: Búsqueda por patrones vs. Búsqueda por metadatos.
3. **Escaneo y Selección**: Detección de directorios candidatos con opción de fallback si faltan metadatos.
4. **Clasificación y Resumen**: Muestra vista previa de transformaciones propuestas.
5. **Renombrado**: Procesa lotes con resolución interactiva de duplicados.

## Estructura del Proyecto
```
Renombrar_Archivos/
├── src/
│   └── renombrar/
│       ├── core/
│       │   ├── extractor_metadatos.py # Detección y extracción EXIF/video
│       │   ├── file_utils.py          # Utilidades de archivos y búsqueda
│       │   ├── date_utils.py          # Parsing y validación de fechas
│       │   └── procesador_archivos.py # Clasificación y renombrado en lote
│       ├── ui/
│       │   ├── menu_criterio.py       # Menú inicial de selección de criterio
│       │   └── menu.py                # Interfaz de usuario principal
│       └── main.py                    # Orquestador general CLI
├── renombrarfotos.py                  # Punto de entrada
├── requirements.txt                   # Dependencias
└── setup.py                           # Empaquetado
```

## Licencia y Autor
- **Autor**: Jorge Osvaldo Tripodi (JOT) - [@JorgeTrip](https://github.com/JorgeTrip)
- **Licencia**: MIT - ver archivo LICENSE
- Copyright © 2025