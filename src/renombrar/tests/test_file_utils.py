"""
Pruebas unitarias para el módulo file_utils.
"""

import unittest
import os
import tempfile
from datetime import datetime
from ..core.file_utils import (
    obtener_nombre_destino,
    obtener_nombre_destino_letra,
    renombrar_archivo,
    buscar_archivos
)

class TestFileUtils(unittest.TestCase):
    """Clase para probar las funciones del módulo file_utils."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.temp_dir = tempfile.mkdtemp()
        self.archivos_prueba = [
            "IMG_20230101_123456.jpg",
            "IMG_20230101_123457.jpg",
            "IMG_20230101_123458.jpg",
            "IMG-20230101-WA0000.jpg",
            "IMG-20230101-WA0001.jpg",
            "video.mp4",
            "audio.wav"
        ]
        
        # Crear archivos de prueba
        for archivo in self.archivos_prueba:
            with open(os.path.join(self.temp_dir, archivo), 'w') as f:
                f.write('')
    
    def tearDown(self):
        """Limpieza después de las pruebas."""
        for archivo in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, archivo))
        os.rmdir(self.temp_dir)
    
    def test_obtener_nombre_destino(self):
        """Prueba la función obtener_nombre_destino."""
        # Prueba con un archivo que tiene fecha en el nombre
        nombre = "IMG_20230101_123456.jpg"
        nuevo_nombre = obtener_nombre_destino(nombre, 0)
        self.assertEqual(nuevo_nombre, "20230101_123456.jpg")
        
        # Prueba con un archivo que no tiene fecha en el nombre
        nombre = "foto.jpg"
        nuevo_nombre = obtener_nombre_destino(nombre, 0)
        self.assertNotEqual(nuevo_nombre, nombre)
    
    def test_obtener_nombre_destino_letra(self):
        """Prueba la función obtener_nombre_destino_letra."""
        nombre = "IMG_20230101_123456.jpg"
        nuevo_nombre = obtener_nombre_destino_letra(nombre, 'a')
        self.assertEqual(nuevo_nombre, "20230101_123456_a.jpg")
        
        # Prueba con letra inválida
        nuevo_nombre = obtener_nombre_destino_letra(nombre, 'x')
        self.assertIsNone(nuevo_nombre)
    
    def test_renombrar_archivo(self):
        """Prueba la función renombrar_archivo."""
        nombre_original = "IMG_20230101_123456.jpg"
        nombre_nuevo = "20230101_123456.jpg"
        
        ruta_original = os.path.join(self.temp_dir, nombre_original)
        ruta_nueva = os.path.join(self.temp_dir, nombre_nuevo)
        
        # Verificar que el archivo original existe
        self.assertTrue(os.path.exists(ruta_original))
        
        # Renombrar el archivo
        resultado = renombrar_archivo(ruta_original, ruta_nueva)
        self.assertTrue(resultado)
        
        # Verificar que el archivo original ya no existe
        self.assertFalse(os.path.exists(ruta_original))
        # Verificar que el archivo nuevo existe
        self.assertTrue(os.path.exists(ruta_nueva))
    
    def test_buscar_archivos(self):
        """Prueba la función buscar_archivos."""
        extensiones = (".jpg", ".mp4", ".wav")
        archivos_img, archivos_vid, otros_archivos, archivos_telefono = buscar_archivos(
            self.temp_dir, extensiones
        )
        
        # Verificar que se encontraron los archivos correctamente
        self.assertEqual(len(archivos_img), 3)  # Los 3 archivos .jpg
        self.assertEqual(len(archivos_vid), 1)  # El archivo .mp4
        self.assertEqual(len(otros_archivos), 1)  # El archivo .wav
        self.assertEqual(len(archivos_telefono), 2)  # Los 2 archivos con formato WA

if __name__ == '__main__':
    unittest.main() 