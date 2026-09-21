"""
Pruebas unitarias para el módulo date_utils.
"""

import unittest
from renombrar.core.date_utils import (
    obtener_fecha_hora,
    obtener_fecha_hora_desde_nombre,
    archivo_tiene_formato_destino,
    tiene_formato_telefono
)

class TestDateUtils(unittest.TestCase):
    """Clase para probar las funciones del módulo date_utils."""

    def test_obtener_fecha_hora_con_fecha_y_hora(self):
        """Prueba la extracción de fecha y hora cuando están presentes en el nombre."""
        nombre = "IMG_20230101_123456.jpg"
        fecha, hora = obtener_fecha_hora(nombre)
        self.assertEqual(fecha, "2023-01-01")
        self.assertEqual(hora, "12-34-56")

    def test_obtener_fecha_hora_sin_fecha(self):
        """Prueba con un archivo que no tiene fecha en el nombre."""
        nombre = "foto.jpg"
        fecha, hora = obtener_fecha_hora(nombre)
        self.assertIsNone(fecha)
        self.assertIsNone(hora)

    def test_obtener_fecha_hora_desde_nombre_formatos(self):
        """Prueba con diferentes formatos de fecha en el nombre."""
        casos = [
            ("IMG_20230101_123456.jpg", "2023-01-01", "12-34-56"),
            ("20230101_123456.jpg", "2023-01-01", "12-34-56"),
            ("2023-01-01 12-34-56.jpg", "2023-01-01", "12-34-56"),
            ("2023-01-01.jpg", "2023-01-01", None)
        ]
        for nombre, exp_fecha, exp_hora in casos:
            fecha, hora = obtener_fecha_hora_desde_nombre(nombre)
            self.assertEqual(fecha, exp_fecha)
            self.assertEqual(hora, exp_hora)

    def test_archivo_tiene_formato_destino(self):
        """Prueba la función archivo_tiene_formato_destino."""
        nombres_validos = [
            "2023-01-01 12-34-56 - foto.jpg",
            "2023-01-01 12-34-56 - IMG_1234.jpg"
        ]
        for nombre in nombres_validos:
            self.assertTrue(archivo_tiene_formato_destino(nombre))

        nombres_invalidos = [
            "foto.jpg",
            "IMG_20230101_123456.jpg",
            "20230101_123456.jpg"
        ]
        for nombre in nombres_invalidos:
            self.assertFalse(archivo_tiene_formato_destino(nombre))

    def test_tiene_formato_telefono(self):
        """Prueba la función tiene_formato_telefono."""
        nombres_validos = [
            "20230101_123456.jpg",
            "20241225_090000.mp4"
        ]
        for nombre in nombres_validos:
            self.assertTrue(tiene_formato_telefono(nombre))

        nombres_invalidos = [
            "foto.jpg",
            "IMG_20230101_123456.jpg",
            "VID_20230101_123456.mp4"
        ]
        for nombre in nombres_invalidos:
            self.assertFalse(tiene_formato_telefono(nombre))

if __name__ == "__main__":
    unittest.main()