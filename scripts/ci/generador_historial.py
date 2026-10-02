"""Módulo generador y sincronizador de historiales de cambio (Changelog).

Actualiza automáticamente 'CHANGELOG.md' y 'changelog.json' manteniendo
el estándar de desarrollo y versionado semántico de Jorge.
"""

from typing import List, Dict, Any


def formatear_entrada_markdown(version: str, fecha: str, commits: List[str]) -> str:
    """Construye un bloque de texto en formato Markdown para una versión específica.

    Args:
        version: Cadena con la versión semántica (ej. '1.9.0').
        fecha: Fecha en formato YYYY-MM-DD.
        commits: Lista de mensajes de commits incluidos en la versión.

    Returns:
        Texto en Markdown listo para ser insertado.
    """
    lineas = [f"## [{version}] - {fecha}"]
    for commit in commits:
        texto = commit.strip()
        if texto:
            lineas.append(f"- {texto}")
    return "\n".join(lineas) + "\n"


def actualizar_changelog_json(
    historial_existente: List[Dict[str, Any]],
    version: str,
    fecha: str,
    commits: List[str]
) -> List[Dict[str, Any]]:
    """Agrega la nueva versión al inicio de la lista del historial JSON.

    Args:
        historial_existente: Lista de diccionarios con versiones previas.
        version: Nueva versión semántica.
        fecha: Fecha de publicación.
        commits: Lista de cambios o commits.

    Returns:
        Nueva lista con la versión añadida en el primer lugar.
    """
    # Evitar duplicar la misma versión si ya fue procesada
    historial_filtrado = [e for e in historial_existente if e.get("version") != version]
    nueva_entrada = {
        "version": version,
        "fecha": fecha,
        "cambios": commits
    }
    return [nueva_entrada] + historial_filtrado


import re

def actualizar_changelog_markdown(
    contenido_existente: str,
    version: str,
    fecha: str,
    commits: List[str]
) -> str:
    """Inserta la nueva sección de cambios en CHANGELOG.md inmediatamente tras el encabezado.

    Si la versión ya existía previamente, la reemplaza de manera idempotente.

    Args:
        contenido_existente: Contenido actual de CHANGELOG.md.
        version: Nueva versión semántica.
        fecha: Fecha de publicación.
        commits: Lista de mensajes de commits.

    Returns:
        Contenido Markdown actualizado.
    """
    bloque_nuevo = formatear_entrada_markdown(version, fecha, commits)
    titulo_principal = "# Historial de Cambios (Changelog)"

    # Limpiar cualquier bloque previo de la misma versión si existía
    patron_previa = rf"##\s*\[{re.escape(version)}\][\s\S]*?(?=(?:##\s*\[|\Z))"
    texto_sin_version = re.sub(patron_previa, "", contenido_existente).strip()

    if not texto_sin_version:
        return f"{titulo_principal}\n\n{bloque_nuevo}"

    if titulo_principal in texto_sin_version:
        partes = texto_sin_version.split(titulo_principal, 1)
        resto = partes[1].lstrip("\r\n")
        return f"{titulo_principal}\n\n{bloque_nuevo}\n{resto}".rstrip() + "\n"

    return f"{titulo_principal}\n\n{bloque_nuevo}\n{texto_sin_version}".rstrip() + "\n"
