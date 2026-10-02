import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.ci.actualizador_archivos import (
    actualizar_texto_setup_py,
    actualizar_texto_menu_py,
    actualizar_texto_readme
)

class TestActualizadorArchivos(unittest.TestCase):
    """Pruebas unitarias para la sincronización de versiones en los archivos de la app."""

    def test_actualizar_setup_py(self):
        """Verifica el reemplazo del campo version en setup.py."""
        contenido = 'setup(\n    name="renombrar",\n    version="1.8.0",\n    packages=[]\n)'
        resultado = actualizar_texto_setup_py(contenido, "1.9.0")
        self.assertIn('version="1.9.0"', resultado)
        self.assertNotIn('version="1.8.0"', resultado)

    def test_actualizar_menu_py(self):
        """Verifica la actualización del título de versión en menu.py."""
        contenido = 'titulo = "Renombrar archivos de fotos y videos - v1.8"'
        resultado = actualizar_texto_menu_py(contenido, "1.9.0")
        self.assertIn('v1.9.0', resultado)

    def test_actualizar_readme(self):
        """Verifica la actualización del encabezado principal en README.md."""
        contenido = '# Renombrar Archivos de Fotos y Videos - v1.8\n\nDescripción del proyecto.'
        resultado = actualizar_texto_readme(contenido, "1.9.0")
        self.assertIn('# Renombrar Archivos de Fotos y Videos - v1.9.0', resultado)

if __name__ == "__main__":
    unittest.main()
