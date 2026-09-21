"""
Pruebas unitarias para procesador_archivos.py.
"""

import os
import tempfile
import unittest

from renombrar.core.procesador_archivos import (
    clasificar_archivos_por_patron,
    ejecutar_renombrado_lote
)

class TestProcesadorArchivos(unittest.TestCase):
    """Pruebas para clasificación y ejecución de renombrado."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except Exception:
                    pass
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass

    def test_clasificar_archivos_por_patron(self):
        """Valida que los archivos encontrados se clasifiquen según su prefijo y extensión."""
        archivos_dir = {
            ".": ["IMG_20230101_120000.jpg", "VID_20230101_130000.mp4", "20230101_140000.mp4"]
        }
        extensiones = (".jpg", ".jpeg", ".png", ".mkv", ".mp4", ".heic")
        clasificados = clasificar_archivos_por_patron(archivos_dir, ["."], extensiones)

        self.assertEqual(len(clasificados['archivos_img']), 1)
        self.assertEqual(len(clasificados['archivos_vid']), 1)
        self.assertEqual(len(clasificados['archivos_telefono']), 1)

    def test_ejecutar_renombrado_lote(self):
        """Valida la ejecución del renombrado en lote sobre archivos reales."""
        nombre_orig = "test_archivo.jpg"
        ruta_orig = os.path.join(self.temp_dir, nombre_orig)
        with open(ruta_orig, "w") as f:
            f.write("contenido de prueba")

        nuevo_nombre = "2023-01-01 12-00-00 - test_archivo.jpg"
        lote = [(".", nombre_orig, nuevo_nombre)]

        cant_renombrados, cambios = ejecutar_renombrado_lote(
            lote, self.temp_dir, callback_duplicado=lambda orig, dest: 'b'
        )

        self.assertEqual(cant_renombrados, 1)
        self.assertEqual(cambios, [(nombre_orig, nuevo_nombre)])
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, nuevo_nombre)))

if __name__ == "__main__":
    unittest.main()
