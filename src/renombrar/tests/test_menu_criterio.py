"""
Pruebas unitarias para el módulo ui/menu_criterio.py.
"""

import unittest
from unittest.mock import patch

from renombrar.ui.menu_criterio import (
    seleccionar_criterio_renombrado,
    confirmar_renombrado_sin_hora,
    preguntar_usar_fallback,
    CRITERIO_PATRONES,
    CRITERIO_METADATOS,
    CRITERIO_SALIR
)

class TestMenuCriterio(unittest.TestCase):
    """Pruebas del menú de selección de criterio y confirmaciones."""

    @patch('builtins.input', side_effect=['1'])
    def test_seleccionar_criterio_patrones(self, mock_input):
        criterio = seleccionar_criterio_renombrado()
        self.assertEqual(criterio, CRITERIO_PATRONES)

    @patch('builtins.input', side_effect=['2'])
    def test_seleccionar_criterio_metadatos(self, mock_input):
        criterio = seleccionar_criterio_renombrado()
        self.assertEqual(criterio, CRITERIO_METADATOS)

    @patch('builtins.input', side_effect=['3'])
    def test_seleccionar_criterio_salir(self, mock_input):
        criterio = seleccionar_criterio_renombrado()
        self.assertEqual(criterio, CRITERIO_SALIR)

    @patch('builtins.input', side_effect=['invalid', '2'])
    def test_seleccionar_criterio_reintento_valido(self, mock_input):
        criterio = seleccionar_criterio_renombrado()
        self.assertEqual(criterio, CRITERIO_METADATOS)

    @patch('builtins.input', side_effect=['s'])
    def test_confirmar_renombrado_sin_hora_afirmativo(self, mock_input):
        resultado = confirmar_renombrado_sin_hora("foto.jpg", "2023-01-01 - foto.jpg")
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=['n'])
    def test_confirmar_renombrado_sin_hora_negativo(self, mock_input):
        resultado = confirmar_renombrado_sin_hora("foto.jpg", "2023-01-01 - foto.jpg")
        self.assertFalse(resultado)

    @patch('builtins.input', side_effect=['s'])
    def test_preguntar_usar_fallback_afirmativo_con_dict(self, mock_input):
        archivos_sin = {
            "Subcarpeta A": ["foto1.jpg", "foto2.jpg"],
            "Subcarpeta B": ["video1.mp4"]
        }
        resultado = preguntar_usar_fallback(archivos_sin)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=['n'])
    def test_preguntar_usar_fallback_negativo_con_dict(self, mock_input):
        archivos_sin = {
            ".": ["foto_suelta.jpg"]
        }
        resultado = preguntar_usar_fallback(archivos_sin)
        self.assertFalse(resultado)

if __name__ == "__main__":
    unittest.main()
