# Renombrar Archivos de Fotos y Videos - v1.8

Una herramienta profesional en Python para renombrar automáticamente archivos de fotos y videos, agregando la fecha y hora extraída del nombre del archivo al inicio del nombre, optimizando la organización cronológica de tu biblioteca multimedia.

## Características Principales

### 🖥️ Interfaz de Usuario Mejorada
- **Pantalla de Bienvenida Interactiva**: Muestra ejemplos de transformaciones antes de iniciar
- **Título Centrado**: Presentación profesional con título adaptado al ancho de la terminal
- **Copyright Integrado**: Información de autoría visible en el título y al salir del programa
- **Confirmación del Usuario**: Pide consentimiento antes de procesar archivos
- **Limpieza de Pantalla**: Interfaz limpia y organizada durante toda la ejecución

### 📁 Gestión Inteligente de Archivos
- **Búsqueda Recursiva**: Analiza el directorio actual y todos sus subdirectorios
- **Selección Flexible de Directorios**: Elige qué carpetas específicas procesar
- **Múltiples Opciones de Procesamiento**: Selecciona por categorías o procesa todo
- **Prevención de Colisiones**: Maneja archivos duplicados agregando letras secuenciales

### 🔄 Transformaciones de Nombres

El programa reconoce varios patrones y los transforma al formato estándar:

#### Archivos de Imagen (IMG)
```
IMG_20230315_143022.jpg
→ 2023-03-15 14-30-22 - IMG_20230315_143022.jpg
```

#### Archivos de Teléfono (Formato YYYYMMDD_HHMMSS)
```
20231225_090000.mp4
→ 2023-12-25 09-00-00 - 20231225_090000.mp4
```

#### Archivos de Video (VID)
```
VID_20240101_120000.mkv
→ 2024-01-01 12-00-00 - VID_20240101_120000.mkv
```

#### Otros Patrones Reconocidos
```
Canon_20230101_123000.cr2
→ 2023-01-01 12-30-00 - Canon_20230101_123000.cr2

Photo2024-03-15.png
→ 2024-03-15 - Photo2024-03-15.png
```

### 📊 Categorización Automática

Los archivos se agrupan en categorías para control granular:

1. **Archivos IMG**: Imágenes que comienzan con `IMG_`
2. **Archivos VID**: Videos que comienzan con `VID_`
3. **Archivos de Teléfono**: Formato `YYYYMMDD_HHMMSS`
4. **Otros Archivos**: Con extensiones válidas pero otros patrones
5. **Archivos Sugeridos**: Con patrones reconocibles pero extensiones no estándar

### 🎯 Formatos Soportados

**Imágenes**: `.jpg`, `.jpeg`, `.png`, `.heic`  
**Videos**: `.mkv`, `.mp4`

### 🛡️ Seguridad y Prevención de Errores

- Manejo de duplicados con opciones interactivas
- Traceback detallado si ocurren errores
- Ventana de consola siempre visible para depuración
- Confirmación antes de procesar archivos

## Requisitos

- Python 3.6 o superior
- Windows 10/11 (adaptable a otros sistemas)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JorgeTrip/Renombrar_Archivos.git
cd Renombrar_Archivos
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar PyInstaller (para compilar)

```bash
pip install pyinstaller
```

## Formas de Uso

### 1. Como Script de Python

Ejecuta directamente desde el directorio del proyecto:

```bash
python renombrarfotos.py
```

### 2. Como Ejecutable Independiente

Compila el programa a un archivo `.exe` utilizando el script automatizado (recomendado):

```bash
python scripts/crear_ejecutable.py
```

O usando PyInstaller directamente con el archivo spec:

```bash
python -m PyInstaller scripts/RenombrarFotos.spec --clean
```

El ejecutable se creará en `dist/RenombrarFotos.exe` y es completamente independiente.

### 3. Como Paquete Instalado (Modo Desarrollo)

```bash
pip install -e .
```

Luego usa el comando `renombrar` desde cualquier directorio.

## Flujo de Trabajo del Programa

1. **Pantalla de Bienvenida**
   - Muestra título centrado
   - Presenta ejemplos de transformaciones
   - Solicita confirmación del usuario

2. **Búsqueda de Archivos**
   - Escanea recursivamente el directorio actual
   - Identifica archivos con patrones reconocibles
   - Agrupa por directorio

3. **Selección de Directorios**
   - Lista todos los directorios con archivos encontrados
   - Permite seleccionar uno, varios o todos

4. **Clasificación y Resumen**
   - Clasifica archivos por categoría
   - Muestra resumen con transformaciones propuestas
   - Formato: `nombre_original → nombre_nuevo`

5. **Menú de Opciones**
   - Todos los archivos
   - Solo archivos IMG
   - Solo archivos VID
   - Solo archivos de teléfono
   - Combinaciones específicas
   - Salir sin cambios

6. **Procesamiento**
   - Renombra los archivos seleccionados
   - Maneja duplicados interactivamente
   - Muestra resumen de cambios realizados

7. **Continuar o Salir**
   - Opción de procesar más archivos
   - Salida limpia del programa

## Estructura del Proyecto

```
Renombrar_Archivos/
├── src/
│   └── renombrar/
│       ├── core/
│       │   ├── file_utils.py    # Utilidades de archivos y búsqueda
│       │   └── date_utils.py    # Extracción de fecha/hora
│       ├── ui/
│       │   └── menu.py          # Interfaz de usuario
│       └── main.py              # Lógica principal
├── dist/                        # Ejecutables compilados
├── build/                       # Archivos temporales de compilación
├── renombrarfotos.py           # Punto de entrada
├── renombrarfotos.spec         # Configuración de PyInstaller
├── requirements.txt            # Dependencias
├── setup.py                    # Configuración del paquete
└── README.md
```

## Desarrollo y Compilación

### Modo Desarrollo

```bash
pip install -e .
```

Los cambios se reflejan inmediatamente sin necesidad de reinstalar.

### Compilar Ejecutable

```bash
python -m PyInstaller renombrarfotos.spec
```

> **Nota**: Si el comando `pyinstaller` no se encuentra en el PATH, usa `python -m PyInstaller` en su lugar.

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Jorge Osvaldo Tripodi (JOT) - [@JorgeTrip](https://github.com/JorgeTrip)
Copyright © 2025

## Agradecimientos

- A todos los contribuidores que han ayudado a mejorar este proyecto
- A la comunidad de Python por las excelentes herramientas disponibles