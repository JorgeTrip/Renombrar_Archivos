import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.ci.orquestar_release import preparar_datos_release

class TestOrquestarRelease(unittest.TestCase):
    """Pruebas unitarias para la preparación de datos del release."""

    def test_preparar_datos_release_con_commits(self):
        """Verifica que se procesen commits correctamente calculando la nueva versión."""
        ultimo_tag = "1.8.0"
        commits = ["feat: Se agregó exportación", "fix: Se corrigió bug"]
        version, fecha, notas = preparar_datos_release(ultimo_tag, commits)
        
        self.assertEqual(version, "1.9.0")
        self.assertTrue(len(fecha) == 10)  # YYYY-MM-DD
        self.assertIn("feat: Se agregó exportación", notas)

    def test_preparar_datos_release_sin_commits(self):
        """Verifica comportamiento cuando no hay nuevos commits detectados."""
        ultimo_tag = "1.8.0"
        commits = []
        version, fecha, notas = preparar_datos_release(ultimo_tag, commits)
        
        self.assertEqual(version, "1.8.1")
        self.assertIn("Mantenimiento y compilación de release", notas)

if __name__ == "__main__":
    unittest.main()
