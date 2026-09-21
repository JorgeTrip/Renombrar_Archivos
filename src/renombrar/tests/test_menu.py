"""
Pruebas unitarias para el módulo menu.
"""

import unittest
from unittest.mock import patch
from renombrar.ui.menu import (
    mostrar_resumen_archivos,
    mostrar_menu,
    mostrar_opciones_duplicado,
    preguntar_continuar
)

class TestMenu(unittest.TestCase):
    """Clase para probar las funciones del módulo menu."""

    def test_mostrar_resumen_archivos(self):
        """Prueba la función mostrar_resumen_archivos con diccionario clasificado."""
        archivos_clasificados = {
            'archivos_telefono': [("dir", "20230101_123456.jpg", "2023-01-01 12-34-56 - 20230101_123456.jpg")],
            'archivos_img': [("dir", "IMG_20230101_123456.jpg", "2023-01-01 12-34-56 - IMG_20230101_123456.jpg")],
            'archivos_vid': [],
            'otros_archivos': [],
            'archivos_sugeridos': []
        }
        self.assertTrue(mostrar_resumen_archivos(archivos_clasificados))

        clasificados_vacios = {
            'archivos_telefono': [],
            'archivos_img': [],
            'archivos_vid': [],
            'otros_archivos': [],
            'archivos_sugeridos': []
        }
        self.assertFalse(mostrar_resumen_archivos(clasificados_vacios))

    @patch('builtins.input', side_effect=['1'])
    def test_mostrar_menu_opcion_todos(self, mock_input):
        """Prueba mostrar_menu seleccionando la primera opción (todos los archivos)."""
        archivos_clasificados = {
            'archivos_img': [("dir", "IMG.jpg", "nuevo.jpg")]
        }
        resultado = mostrar_menu(archivos_clasificados)
        self.assertIsNotNone(resultado)
        self.assertIn('archivos_img', resultado)

    @patch('builtins.input', side_effect=['a'])
    def test_mostrar_opciones_duplicado_opcion_a(self, mock_input):
        """Prueba la opción 'a' en caso de archivo duplicado."""
        opcion = mostrar_opciones_duplicado("foto.jpg", "2023-01-01 - foto.jpg")
        self.assertEqual(opcion, 'a')

    @patch('builtins.input', side_effect=['b'])
    def test_mostrar_opciones_duplicado_opcion_b(self, mock_input):
        """Prueba la opción 'b' en caso de archivo duplicado."""
        opcion = mostrar_opciones_duplicado("foto.jpg", "2023-01-01 - foto.jpg")
        self.assertEqual(opcion, 'b')

    @patch('builtins.input', side_effect=['s', 'n'])
    def test_preguntar_continuar(self, mock_input):
        """Prueba la confirmación de continuar el ciclo."""
        self.assertTrue(preguntar_continuar())
        self.assertFalse(preguntar_continuar())

if __name__ == '__main__':
    unittest.main()