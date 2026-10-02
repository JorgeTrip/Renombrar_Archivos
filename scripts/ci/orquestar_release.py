"""Script principal de orquestación para la generación de releases en CI/CD.

Calcula la nueva versión, actualiza archivos de código, CHANGELOG.md y changelog.json,
y emite las variables necesarias para el workflow de GitHub Actions.
"""

import datetime
import json
import os
import subprocess
import sys
from typing import List, Tuple

# Asegurar que la raíz del proyecto esté en sys.path al ejecutarse como script directo
_raiz_ci = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _raiz_ci not in sys.path:
    sys.path.insert(0, _raiz_ci)

from scripts.ci.actualizador_archivos import sincronizar_version_en_proyecto
from scripts.ci.analizador_version import analizar_siguiente_version
from scripts.ci.generador_historial import (
    actualizar_changelog_json,
    actualizar_changelog_markdown,
    formatear_entrada_markdown
)


def obtener_ultimo_tag_git() -> str:
    """Obtiene el último tag de Git o retorna '1.8.0' como base inicial."""
    try:
        resultado = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        tag = resultado.stdout.strip()
        return tag if tag else "1.8.0"
    except Exception:
        return "1.8.0"


def obtener_commits_desde_tag(ultimo_tag: str) -> List[str]:
    """Obtiene los mensajes de commits desde el último tag hasta HEAD."""
    try:
        rango = f"{ultimo_tag}..HEAD" if ultimo_tag else "HEAD"
        resultado = subprocess.run(
            ["git", "log", rango, "--pretty=format:%s"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        lineas = [l.strip() for l in resultado.stdout.splitlines() if l.strip()]
        # Filtrar commits generados por el bot para no ciclar
        return [l for l in lineas if "[skip ci]" not in l]
    except Exception:
        return []


def preparar_datos_release(ultimo_tag: str, commits: List[str]) -> Tuple[str, str, str]:
    """Calcula versión, fecha actual y notas de la versión.

    Returns:
        Tupla con (nueva_version, fecha_iso, notas_markdown)
    """
    fecha = datetime.date.today().isoformat()
    if not commits:
        nueva_version = analizar_siguiente_version(ultimo_tag, ["fix: Mantenimiento"])
        commits_usados = ["fix: Mantenimiento y compilación de release"]
    else:
        nueva_version = analizar_siguiente_version(ultimo_tag, commits)
        commits_usados = commits

    notas_md = formatear_entrada_markdown(nueva_version, fecha, commits_usados)
    return nueva_version, fecha, notas_md


def procesar_historiales(raiz: str, version: str, fecha: str, commits: List[str]) -> None:
    """Actualiza y guarda CHANGELOG.md y changelog.json."""
    ruta_md = os.path.join(raiz, "CHANGELOG.md")
    contenido_md = ""
    if os.path.exists(ruta_md):
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido_md = f.read()

    nuevo_md = actualizar_changelog_markdown(contenido_md, version, fecha, commits)
    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write(nuevo_md)

    ruta_json = os.path.join(raiz, "changelog.json")
    datos_json = []
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                datos_json = json.load(f)
        except Exception:
            datos_json = []

    nuevo_json = actualizar_changelog_json(datos_json, version, fecha, commits)
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(nuevo_json, f, indent=2, ensure_ascii=False)


def ejecutar_orquestacion():
    """Punto de entrada CLI para GitHub Actions."""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ultimo_tag = obtener_ultimo_tag_git()
    commits = obtener_commits_desde_tag(ultimo_tag)
    version, fecha, notas = preparar_datos_release(ultimo_tag, commits)

    print(f"Versión anterior: {ultimo_tag}")
    print(f"Nueva versión calculada: {version}")

    sincronizar_version_en_proyecto(raiz, version)
    commits_reales = commits if commits else ["fix: Mantenimiento y compilación de release"]
    procesar_historiales(raiz, version, fecha, commits_reales)

    # Escribir notas del release temporal para GitHub Actions
    ruta_notas = os.path.join(raiz, "release_notes.md")
    with open(ruta_notas, "w", encoding="utf-8") as f:
        f.write(notas)

    # Si se ejecuta en GitHub Actions, exportar al output
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output and os.path.exists(github_output):
        with open(github_output, "a", encoding="utf-8") as gh_out:
            gh_out.write(f"version={version}\n")
            gh_out.write(f"tag=v{version}\n")


if __name__ == "__main__":
    ejecutar_orquestacion()
