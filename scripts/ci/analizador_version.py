"""Módulo analizador de versiones semánticas y mensajes de commit.

Este módulo implementa las reglas de versionado semántico automatizado
basadas en las directrices de desarrollo de Jorge (Regla #7).
"""

import re
from typing import List


def determinar_incremento(mensajes_commits: List[str]) -> str:
    """Determina si el incremento debe ser 'major', 'minor' o 'patch'.

    Prioridades según Regla #7:
    - BREAKING: -> 'major'
    - feat: o 🚀 -> 'minor'
    - fix: o 🔧 o cualquier otro commit -> 'patch'

    Args:
        mensajes_commits: Lista de mensajes de commits a evaluar.

    Returns:
        Cadena con el tipo de incremento: 'major', 'minor' o 'patch'.
    """
    tiene_breaking = False
    tiene_feat = False

    for mensaje in mensajes_commits:
        texto = mensaje.strip()
        if "BREAKING:" in texto or "BREAKING CHANGE" in texto:
            tiene_breaking = True
            break
        if texto.startswith("feat:") or "🚀" in texto or "feat(" in texto:
            tiene_feat = True

    if tiene_breaking:
        return "major"
    if tiene_feat:
        return "minor"
    return "patch"


def normalizar_version(version_str: str) -> List[int]:
    """Parsea una cadena de versión a una lista de 3 enteros [major, minor, patch].

    Maneja prefijos comunes como 'v' y formatos de dos números como '1.8'.

    Args:
        version_str: Cadena de versión (ej. '1.8', 'v1.8.0').

    Returns:
        Lista de 3 enteros representando [major, minor, patch].
    """
    limpio = version_str.strip().lstrip("vV")
    partes = re.findall(r"\d+", limpio)
    
    major = int(partes[0]) if len(partes) > 0 else 1
    minor = int(partes[1]) if len(partes) > 1 else 0
    patch = int(partes[2]) if len(partes) > 2 else 0

    return [major, minor, patch]


def incrementar_version(version_actual: str, tipo_incremento: str) -> str:
    """Calcula la siguiente versión semántica basada en el tipo de incremento.

    Args:
        version_actual: Versión base (ej. '1.8.0' o '1.8').
        tipo_incremento: 'major', 'minor' o 'patch'.

    Returns:
        Cadena formateada con la nueva versión (ej. '1.9.0').
    """
    major, minor, patch = normalizar_version(version_actual)

    if tipo_incremento == "major":
        major += 1
        minor = 0
        patch = 0
    elif tipo_incremento == "minor":
        minor += 1
        patch = 0
    else:  # 'patch'
        patch += 1

    return f"{major}.{minor}.{patch}"


def analizar_siguiente_version(ultimo_tag: str, commits: List[str]) -> str:
    """Orquesta la determinación del incremento y cálculo de la siguiente versión.

    Args:
        ultimo_tag: Última etiqueta de git encontrada.
        commits: Lista de mensajes de commits desde el último tag.

    Returns:
        Cadena con la versión semántica calculada.
    """
    tipo = determinar_incremento(commits)
    return incrementar_version(ultimo_tag, tipo)
