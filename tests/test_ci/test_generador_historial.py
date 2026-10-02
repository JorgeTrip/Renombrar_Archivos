import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.ci.generador_historial import (
    formatear_entrada_markdown,
    actualizar_changelog_json,
    actualizar_changelog_markdown
)

class TestGeneradorHistorial(unittest.TestCase):
    """Pruebas unitarias para la generación de CHANGELOG.md y changelog.json."""

    def test_formatear_entrada_markdown(self):
        """Verifica la generación del bloque Markdown para una versión."""
        version = "1.9.0"
        fecha = "2026-10-02"
        commits = [
            "feat: Se implementó renombramiento por metadatos",
            "fix: Se corrigió huso horario en videos"
        ]
        resultado = formatear_entrada_markdown(version, fecha, commits)
        self.assertIn("## [1.9.0] - 2026-10-02", resultado)
        self.assertIn("- feat: Se implementó renombramiento por metadatos", resultado)
        self.assertIn("- fix: Se corrigió huso horario en videos", resultado)

    def test_actualizar_changelog_json(self):
        """Verifica la estructura y persistencia en changelog.json."""
        contenido_existente = [
            {"version": "1.8.0", "fecha": "2025-03-19", "cambios": ["Versión inicial"]}
        ]
        version = "1.9.0"
        fecha = "2026-10-02"
        commits = ["feat: Nueva funcionalidad"]

        nuevo_json = actualizar_changelog_json(contenido_existente, version, fecha, commits)
        self.assertEqual(len(nuevo_json), 2)
        # La versión más reciente debe encabezar la lista
        self.assertEqual(nuevo_json[0]["version"], "1.9.0")
        self.assertEqual(nuevo_json[0]["cambios"], commits)

    def test_actualizar_changelog_markdown(self):
        """Verifica que el nuevo bloque se inserte al inicio tras el título."""
        md_original = "# Historial de Cambios (Changelog)\n\n## [1.8.0] - 2025-03-19\n- Versión base\n"
        version = "1.9.0"
        fecha = "2026-10-02"
        commits = ["feat: Nueva funcionalidad"]

        nuevo_md = actualizar_changelog_markdown(md_original, version, fecha, commits)
        self.assertTrue(nuevo_md.startswith("# Historial de Cambios (Changelog)"))
        self.assertIn("## [1.9.0] - 2026-10-02", nuevo_md)
    def test_actualizar_changelog_markdown_no_duplica_version(self):
        """Verifica que no se duplique una versión si ya existe en el markdown."""
        md_con_version = "# Historial de Cambios (Changelog)\n\n## [1.9.0] - 2026-10-01\n- Versión vieja\n\n## [1.8.0] - 2025-03-19\n- Base\n"
        nuevo_md = actualizar_changelog_markdown(md_con_version, "1.9.0", "2026-10-02", ["feat: Actualización"])
        # Solo debe existir una ocurrencia del encabezado 1.9.0
        self.assertEqual(nuevo_md.count("## [1.9.0]"), 1)
        self.assertIn("feat: Actualización", nuevo_md)

if __name__ == "__main__":
    unittest.main()
