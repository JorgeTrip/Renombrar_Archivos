import unittest
import sys
import os

# Asegurar que la ruta del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.ci.analizador_version import (
    determinar_incremento,
    incrementar_version,
    analizar_siguiente_version
)

class TestAnalizadorVersion(unittest.TestCase):
    """Pruebas unitarias para el análisis y cálculo de versiones semánticas."""

    def test_incremento_patch_por_defecto_o_fix(self):
        """Verifica que mensajes con fix o sin prefijo generen incremento patch."""
        commits_fix = ["fix: Se corrigió error en filtros"]
        self.assertEqual(determinar_incremento(commits_fix), "patch")

        commits_sin_prefijo = ["Se corrigió un detalle visual"]
        self.assertEqual(determinar_incremento(commits_sin_prefijo), "patch")

    def test_incremento_minor_con_feat_o_emoji(self):
        """Verifica que feat: o el emoji de cohete generen incremento minor."""
        commits_feat = [
            "fix: Se ajustó el espaciado",
            "feat: Se agrega exportación a PDF"
        ]
        self.assertEqual(determinar_incremento(commits_feat), "minor")

        commits_emoji = ["🚀 Se agrega nueva vista de galería"]
        self.assertEqual(determinar_incremento(commits_emoji), "minor")

    def test_incremento_major_con_breaking(self):
        """Verifica que BREAKING: tenga máxima precedencia generando incremento major."""
        commits = [
            "feat: Se agrega soporte de videos",
            "BREAKING: Se reemplaza la interfaz CLI por API REST"
        ]
        self.assertEqual(determinar_incremento(commits), "major")

    def test_incrementar_version_patch(self):
        """Verifica el cálculo de nueva versión patch."""
        self.assertEqual(incrementar_version("1.8.0", "patch"), "1.8.1")
        self.assertEqual(incrementar_version("v1.8", "patch"), "1.8.1")

    def test_incrementar_version_minor(self):
        """Verifica el cálculo de nueva versión minor."""
        self.assertEqual(incrementar_version("1.8.2", "minor"), "1.9.0")
        self.assertEqual(incrementar_version("1.8", "minor"), "1.9.0")

    def test_incrementar_version_major(self):
        """Verifica el cálculo de nueva versión major."""
        self.assertEqual(incrementar_version("1.9.3", "major"), "2.0.0")

    def test_analizar_siguiente_version_integrado(self):
        """Prueba integrada de cálculo con tags y commits."""
        ultimo_tag = "1.8"
        commits = [
            "feat: Se implementó renombramiento por metadatos",
            "fix: Se corrigió huso horario en videos"
        ]
        nueva_version = analizar_siguiente_version(ultimo_tag, commits)
        self.assertEqual(nueva_version, "1.9.0")

if __name__ == "__main__":
    unittest.main()
