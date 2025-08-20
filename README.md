# Renombrar Archivos de Fotos y Videos

Una herramienta en Python para renombrar automáticamente archivos de fotos y videos basándose en su fecha de creación o modificación.

## Características

- **Búsqueda Recursiva**: Analiza el directorio actual y todos sus subdirectorios en busca de archivos.
- **Selección de Directorios**: Permite al usuario elegir en qué carpetas específicas desea realizar el renombrado.
- **Renombrado Inteligente**: Asigna nombres con el formato `YYYYMMDD_HHMMSS` basados en metadatos o el nombre original del archivo.
- **Categorización Clara**: Agrupa los archivos en categorías (Imágenes, Videos, Formato Teléfono) para un control granular.
- **Sugerencias de Renombrado**: Identifica archivos que coinciden con un patrón de nombre (ej. `Canon_20230101_123000.cr2`) pero tienen extensiones no estándar y los sugiere para renombrar.
- **Soporte Amplio de Formatos**: Configurado para extensiones comunes de imagen y video (`.jpg`, `.jpeg`, `.png`, `.mkv`, `.mp4`, `.heic`).
- **Prevención de Errores**: La ventana de la consola permanece abierta si ocurre un error, mostrando el traceback para facilitar la depuración.
- **Múltiples Vías de Ejecución**: Puede usarse como un comando global, un `.exe` portable o desde el menú contextual de Windows.

## Requisitos

- Python 3.6 o superior
- Windows 10/11

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

### 3. Instalar el paquete

```bash
pip install -e .
```

## Formas de Uso

### 1. Como comando global

Después de instalar el paquete, puedes usar el comando `renombrar` desde cualquier directorio:

```bash
renombrar
```

### 2. Como ejecutable independiente

1. Navega a la carpeta `scripts/`
2. Ejecuta `compilar.bat`
3. Selecciona la opción 2 para crear el ejecutable
4. El archivo `RenombrarFotos.exe` se creará en la carpeta `dist/`
5. Puedes copiar este .exe a cualquier lugar y ejecutarlo con doble clic

### 3. Desde el menú contextual de Windows

1. Navega a la carpeta `scripts/`
2. Ejecuta `compilar.bat` como administrador
3. Selecciona la opción 1 para registrar en el menú contextual
4. Ahora podrás hacer clic derecho en cualquier carpeta y verás la opción "Renombrar archivos de fotos"

## Uso del Programa

1.  **Ejecución**: Inicia el programa desde la carpeta que deseas organizar.
2.  **Búsqueda**: La aplicación escaneará recursivamente el directorio y subdirectorios en busca de archivos.
3.  **Selección de Directorio**: Si se encuentran archivos en múltiples carpetas, se mostrará una lista para que selecciones en cuáles quieres trabajar.
4.  **Resumen de Cambios**: Se presentará un resumen de los archivos a renombrar, mostrando `nombre_original -> nombre_nuevo`, agrupados por categorías:
    - Archivos de imagen (`IMG_...`)
    - Archivos de video (`VID_...`)
    - Archivos con formato teléfono (`YYYYMMDD_HHMMSS...`)
    - Otros archivos con extensiones válidas.
    - **Sugerencias**: Archivos con un patrón de nombre válido pero extensión no reconocida (ej. `.cr2`, `.dng`).
5.  **Confirmación**: Podrás elegir qué categorías de archivos deseas renombrar. Puedes seleccionar una, varias o todas.
6.  **Renombrado**: La aplicación procederá a renombrar los archivos de las categorías seleccionadas, evitando colisiones de nombres.

## Estructura del Proyecto

```
Renombrar_Archivos/
├── src/
│   └── renombrar/
│       ├── core/
│       │   ├── file_utils.py
│       │   └── date_utils.py
│       ├── ui/
│       │   └── menu.py
│       └── main.py
├── scripts/
│   ├── compilar.bat
│   ├── crear_ejecutable.py
│   └── registrar_menu_contextual.py
├── build/
├── dist/
├── docs/
├── requirements.txt
└── setup.py
```

## Desarrollo

### Compilación

El proyecto incluye un script `compilar.bat` que facilita las tareas de desarrollo:

1. Registrar en menú contextual (requiere admin)
2. Crear ejecutable .exe
3. Instalar paquete en modo desarrollo

### Modo Desarrollo

Para trabajar en el código:

1. Instala el paquete en modo desarrollo:
   ```bash
   pip install -e .
   ```
2. Realiza cambios en el código
3. Los cambios se reflejan inmediatamente sin necesidad de reinstalar

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Jorge Trip - [@JorgeTrip](https://github.com/JorgeTrip)

## Agradecimientos

- A todos los contribuidores que han ayudado a mejorar este proyecto
- A la comunidad de Python por las excelentes herramientas disponibles 