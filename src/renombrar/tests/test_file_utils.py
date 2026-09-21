"""
Pruebas unitarias para el módulo file_utils.
"""

import os
import tempfile
import unittest
from PIL import Image

from renombrar.core.file_utils import (
    formatear_nombre_destino,
    formatear_nombre_destino_letra,
    obtener_nombre_destino,
    renombrar_archivo,
    encontrar_archivos_por_directorio,
    encontrar_archivos_por_metadatos
)

class TestFileUtils(unittest.TestCase):
    """Clase para probar las funciones del módulo file_utils."""

    def setUp(self):
        """Configuración inicial para las pruebas con directorio temporal."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Limpieza tras las pruebas."""
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

    def test_formatear_nombre_destino(self):
        """Prueba la función formatear_nombre_destino con y sin hora."""
        nombre = "foto.jpg"
        res_con_hora = formatear_nombre_destino(nombre, "2023-01-01", "12-00-00")
        self.assertEqual(res_con_hora, "2023-01-01 12-00-00 - foto.jpg")

        res_sin_hora = formatear_nombre_destino(nombre, "2023-01-01", None)
        self.assertEqual(res_sin_hora, "2023-01-01 - foto.jpg")

    def test_formatear_nombre_destino_limpia_prefijo_existente(self):
        """Prueba que si un archivo ya tiene YYYY-MM-DD - se reemplace y no se duplique."""
        nombre_previo = "2023-01-01 - foto.jpg"
        res = formatear_nombre_destino(nombre_previo, "2023-01-01", "14-30-22")
        self.assertEqual(res, "2023-01-01 14-30-22 - foto.jpg")

    def test_obtener_nombre_destino(self):
        """Prueba la función obtener_nombre_destino por patrones de nombre."""
        nombre = "IMG_20230101_123456.jpg"
        nuevo_nombre = obtener_nombre_destino(nombre)
        self.assertEqual(nuevo_nombre, "2023-01-01 12-34-56 - IMG_20230101_123456.jpg")

    def test_renombrar_archivo(self):
        """Prueba la función renombrar_archivo física."""
        ruta_orig = os.path.join(self.temp_dir, "original.txt")
        ruta_dest = os.path.join(self.temp_dir, "destino.txt")
        with open(ruta_orig, "w") as f:
            f.write("contenido")

        self.assertTrue(os.path.exists(ruta_orig))
        exito = renombrar_archivo(ruta_orig, ruta_dest)
        self.assertTrue(exito)
        self.assertFalse(os.path.exists(ruta_orig))
        self.assertTrue(os.path.exists(ruta_dest))

    def test_encontrar_archivos_por_directorio_omite_ya_formateados(self):
        """Prueba que los archivos con formato destino se omitan y se contabilicen."""
        ruta_ya_formateado = os.path.join(self.temp_dir, "2023-01-01 12-00-00 - foto.jpg")
        ruta_candidato = os.path.join(self.temp_dir, "IMG_20230101_130000.jpg")
        for r in [ruta_ya_formateado, ruta_candidato]:
            with open(r, "w") as f:
                f.write("")

        candidatos, omitidos = encontrar_archivos_por_directorio(self.temp_dir)
        archivos_encontrados = [f for lista in candidatos.values() for f in lista]

        self.assertIn("IMG_20230101_130000.jpg", archivos_encontrados)
        self.assertNotIn("2023-01-01 12-00-00 - foto.jpg", archivos_encontrados)
        self.assertEqual(omitidos, 1)

    def test_encontrar_archivos_por_metadatos_enriquece_solo_fecha(self):
        """Prueba que un archivo con solo fecha se ofrezca si los metadatos tienen hora."""
        ruta_solo_fecha = os.path.join(self.temp_dir, "2024-05-20 - camara.jpg")
        img = Image.new("RGB", (5, 5))
        exif = img.getexif()
        exif[306] = "2024:05:20 10:15:30"
        img.save(ruta_solo_fecha, "jpeg", exif=exif)

        ruta_completo = os.path.join(self.temp_dir, "2024-05-20 10-15-30 - final.jpg")
        img.save(ruta_completo, "jpeg", exif=exif)

        con_meta, sin_meta, omitidos = encontrar_archivos_por_metadatos(self.temp_dir, (".jpg",))
        archivos_con = [item[0] for lista in con_meta.values() for item in lista]

        self.assertIn("2024-05-20 - camara.jpg", archivos_con)
        self.assertNotIn("2024-05-20 10-15-30 - final.jpg", archivos_con)
        self.assertEqual(omitidos, 1)

if __name__ == "__main__":
    unittest.main()