"""Módulo de actualización y sincronización de versiones en archivos del proyecto.

Mantiene sincronizados setup.py, README.md y las vistas de usuario con la versión
semántica calculada automáticamente por el CI/CD (Regla #7).
"""

import os
import re


def actualizar_texto_setup_py(contenido: str, nueva_version: str) -> str:
    """Reemplaza la versión en el texto de setup.py.

    Args:
        contenido: Texto fuente de setup.py.
        nueva_version: Versión en formato semver (ej. '1.9.0').

    Returns:
        Texto modificado con la nueva versión.
    """
    patron = r'(version\s*=\s*["\'])([^"\']+)(["\'])'
    return re.sub(patron, rf'\g<1>{nueva_version}\g<3>', contenido)


def actualizar_texto_menu_py(contenido: str, nueva_version: str) -> str:
    """Actualiza la versión en el título del menú de usuario.

    Args:
        contenido: Texto fuente de menu.py.
        nueva_version: Versión en formato semver (ej. '1.9.0').

    Returns:
        Texto modificado con la nueva versión.
    """
    patron = r'(titulo\s*=\s*["\'].*?-\s*v)([\d\.]+)(["\'])'
    return re.sub(patron, rf'\g<1>{nueva_version}\g<3>', contenido)


def actualizar_texto_readme(contenido: str, nueva_version: str) -> str:
    """Actualiza el encabezado de versión principal en README.md.

    Args:
        contenido: Texto fuente de README.md.
        nueva_version: Versión en formato semver (ej. '1.9.0').

    Returns:
        Texto modificado con la nueva versión.
    """
    patron = r'(#\s+Renombrar\s+Archivos.*?-\s*v)([\d\.]+)'
    return re.sub(patron, rf'\g<1>{nueva_version}', contenido)


def sincronizar_version_en_proyecto(raiz_proyecto: str, nueva_version: str) -> None:
    """Aplica la nueva versión en todos los archivos pertinentes del repositorio.

    Args:
        raiz_proyecto: Ruta base del repositorio.
        nueva_version: Versión en formato semver.
    """
    ruta_setup = os.path.join(raiz_proyecto, "setup.py")
    if os.path.exists(ruta_setup):
        with open(ruta_setup, "r", encoding="utf-8") as f:
            contenido = f.read()
        nuevo = actualizar_texto_setup_py(contenido, nueva_version)
        with open(ruta_setup, "w", encoding="utf-8") as f:
            f.write(nuevo)

    ruta_menu = os.path.join(raiz_proyecto, "src", "renombrar", "ui", "menu.py")
    if os.path.exists(ruta_menu):
        with open(ruta_menu, "r", encoding="utf-8") as f:
            contenido = f.read()
        nuevo = actualizar_texto_menu_py(contenido, nueva_version)
        with open(ruta_menu, "w", encoding="utf-8") as f:
            f.write(nuevo)

    ruta_readme = os.path.join(raiz_proyecto, "README.md")
    if os.path.exists(ruta_readme):
        with open(ruta_readme, "r", encoding="utf-8") as f:
            contenido = f.read()
        nuevo = actualizar_texto_readme(contenido, nueva_version)
        with open(ruta_readme, "w", encoding="utf-8") as f:
            f.write(nuevo)
