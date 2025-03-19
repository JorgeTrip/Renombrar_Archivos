"""
Pruebas unitarias para el módulo date_utils.
"""

import unittest
from datetime import datetime
from ..core.date_utils import (
    obtener_fecha_hora,
    obtener_fecha_hora_wav,
    obtener_fecha_hora_desde_nombre,
    archivo_tiene_formato_destino,
    tiene_formato_telefono
)

class TestDateUtils(unittest.TestCase):
    """Clase para probar las funciones del módulo date_utils."""
    
    def test_obtener_fecha_hora(self):
        """Prueba la función obtener_fecha_hora."""
        # Prueba con un archivo que tiene fecha en el nombre
        nombre = "IMG_20230101_123456.jpg"
        fecha = obtener_fecha_hora(nombre)
        self.assertIsInstance(fecha, datetime)
        self.assertEqual(fecha.year, 2023)
        self.assertEqual(fecha.month, 1)
        self.assertEqual(fecha.day, 1)
        self.assertEqual(fecha.hour, 12)
        self.assertEqual(fecha.minute, 34)
        self.assertEqual(fecha.second, 56)
        
        # Prueba con un archivo que no tiene fecha en el nombre
        nombre = "foto.jpg"
        fecha = obtener_fecha_hora(nombre)
        self.assertIsInstance(fecha, datetime)
    
    def test_obtener_fecha_hora_wav(self):
        """Prueba la función obtener_fecha_hora_wav."""
        # Prueba con un archivo WAV
        nombre = "audio.wav"
        fecha = obtener_fecha_hora_wav(nombre)
        self.assertIsInstance(fecha, datetime)
    
    def test_obtener_fecha_hora_desde_nombre(self):
        """Prueba la función obtener_fecha_hora_desde_nombre."""
        # Prueba con diferentes formatos de fecha
        formatos = [
            "IMG_20230101_123456.jpg",
            "20230101_123456.jpg",
            "2023-01-01 12:34:56.jpg",
            "2023/01/01 12:34:56.jpg"
        ]
        
        for nombre in formatos:
            fecha = obtener_fecha_hora_desde_nombre(nombre)
            self.assertIsInstance(fecha, datetime)
            self.assertEqual(fecha.year, 2023)
            self.assertEqual(fecha.month, 1)
            self.assertEqual(fecha.day, 1)
            self.assertEqual(fecha.hour, 12)
            self.assertEqual(fecha.minute, 34)
            self.assertEqual(fecha.second, 56)
    
    def test_archivo_tiene_formato_destino(self):
        """Prueba la función archivo_tiene_formato_destino."""
        # Prueba con archivos que tienen el formato destino
        nombres_validos = [
            "20230101_123456.jpg",
            "20230101_123456_a.jpg",
            "20230101_123456_b.jpg"
        ]
        
        for nombre in nombres_validos:
            self.assertTrue(archivo_tiene_formato_destino(nombre))
        
        # Prueba con archivos que no tienen el formato destino
        nombres_invalidos = [
            "foto.jpg",
            "IMG_20230101_123456.jpg",
            "2023-01-01 12:34:56.jpg"
        ]
        
        for nombre in nombres_invalidos:
            self.assertFalse(archivo_tiene_formato_destino(nombre))
    
    def test_tiene_formato_telefono(self):
        """Prueba la función tiene_formato_telefono."""
        # Prueba con archivos que tienen formato de teléfono
        nombres_validos = [
            "IMG-20230101-WA0000.jpg",
            "IMG-20230101-WA0001.jpg",
            "IMG-20230101-WA9999.jpg"
        ]
        
        for nombre in nombres_validos:
            self.assertTrue(tiene_formato_telefono(nombre))
        
        # Prueba con archivos que no tienen formato de teléfono
        nombres_invalidos = [
            "foto.jpg",
            "IMG_20230101_123456.jpg",
            "20230101_123456.jpg"
        ]
        
        for nombre in nombres_invalidos:
            self.assertFalse(tiene_formato_telefono(nombre))

if __name__ == '__main__':
    unittest.main() 