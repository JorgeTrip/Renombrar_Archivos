# Renombrar Archivos de Fotos y Videos

Una herramienta en Python para renombrar automáticamente archivos de fotos y videos basándose en su fecha de creación o modificación.

## Características

- Renombra archivos de fotos y videos con formato: `YYYYMMDD_HHMMSS`
- Soporta múltiples formatos de archivo:
  - Imágenes: .jpg, .jpeg, .png
  - Videos: .mkv, .mp4
  - Otros: .heic
- Manejo inteligente de archivos duplicados
- Interfaz de línea de comandos intuitiva
- Múltiples formas de ejecución:
  - Como comando global (`renombrar`)
  - Como ejecutable independiente (.exe)
  - Desde el menú contextual de Windows

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

1. Ejecuta el programa de cualquiera de las formas mencionadas arriba
2. El programa buscará automáticamente archivos de fotos y videos en el directorio actual
3. Se mostrará un resumen de los archivos encontrados
4. Selecciona la opción deseada:
   - 1: Renombrar todos los archivos
   - 2: Renombrar solo imágenes
   - 3: Renombrar solo videos
   - 4: Renombrar imágenes y videos
   - 5: Renombrar archivos de teléfono
   - 6: Cancelar

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