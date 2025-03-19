"""
Pruebas unitarias para el módulo menu.
"""

import unittest
from unittest.mock import patch
from ..ui.menu import (
    mostrar_resumen_archivos,
    mostrar_menu,
    mostrar_opciones_duplicado,
    preguntar_continuar
)

class TestMenu(unittest.TestCase):
    """Clase para probar las funciones del módulo menu."""
    
    def test_mostrar_resumen_archivos(self):
        """Prueba la función mostrar_resumen_archivos."""
        archivos_telefono = [("dir", "IMG-20230101-WA0000.jpg")]
        archivos_img = [("dir", "IMG_20230101_123456.jpg")]
        archivos_vid = [("dir", "video.mp4")]
        otros_archivos = [("dir", "audio.wav")]
        
        # Verificar que la función retorna True cuando hay archivos
        self.assertTrue(mostrar_resumen_archivos(
            archivos_telefono, archivos_img, archivos_vid, otros_archivos
        ))
        
        # Verificar que la función retorna False cuando no hay archivos
        self.assertFalse(mostrar_resumen_archivos([], [], [], []))
    
    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7'])
    def test_mostrar_menu(self, mock_input):
        """Prueba la función mostrar_menu."""
        # Probar cada opción válida
        for i in range(1, 7):
            opcion = mostrar_menu()
            self.assertEqual(opcion, i)
        
        # Probar una opción inválida
        with patch('builtins.input', return_value='7'):
            opcion = mostrar_menu()
            self.assertEqual(opcion, 6)  # Debería retornar la opción por defecto
    
    @patch('builtins.input', side_effect=['a', 's', 'x'])
    def test_mostrar_opciones_duplicado(self, mock_input):
        """Prueba la función mostrar_opciones_duplicado."""
        # Probar opción 'a' (agregar letra)
        opcion = mostrar_opciones_duplicado("foto.jpg", "20230101_123456.jpg")
        self.assertEqual(opcion, 'a')
        
        # Probar opción 's' (saltar)
        opcion = mostrar_opciones_duplicado("foto.jpg", "20230101_123456.jpg")
        self.assertEqual(opcion, 's')
        
        # Probar opción inválida
        opcion = mostrar_opciones_duplicado("foto.jpg", "20230101_123456.jpg")
        self.assertEqual(opcion, 's')  # Debería retornar la opción por defecto
    
    @patch('builtins.input', side_effect=['s', 'n', 'x'])
    def test_preguntar_continuar(self, mock_input):
        """Prueba la función preguntar_continuar."""
        # Probar respuesta 's' (sí)
        self.assertTrue(preguntar_continuar())
        
        # Probar respuesta 'n' (no)
        self.assertFalse(preguntar_continuar())
        
        # Probar respuesta inválida
        self.assertFalse(preguntar_continuar())  # Debería retornar False por defecto

if __name__ == '__main__':
    unittest.main() 