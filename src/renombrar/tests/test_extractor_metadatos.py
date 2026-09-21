"""
Pruebas unitarias para el módulo extractor_metadatos y detector de formato.
Fase Roja del ciclo TDD.
"""

import os
import tempfile
import unittest
from PIL import Image

from renombrar.core.extractor_metadatos import (
    detectar_tipo_archivo,
    extraer_metadatos_fecha_hora,
    TIPO_IMAGEN_EXIF,
    TIPO_IMAGEN_HEIC,
    TIPO_VIDEO_MUTAGEN,
    TIPO_VIDEO_HACHOIR,
    TIPO_AUDIO_WAV,
    TIPO_DESCONOCIDO
)

class TestExtractorMetadatos(unittest.TestCase):
    """Pruebas para extracción de metadatos y autodetección de formato."""

    def setUp(self):
        """Crea un directorio temporal para generar archivos de prueba sintéticos."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Elimina los archivos y directorio temporal tras la prueba."""
        for archivo in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, archivo))
            except Exception:
                pass
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass

    def test_detectar_tipo_archivo_por_extension(self):
        """Valida que el detector identifique correctamente el tipo de medio."""
        ruta_jpg = os.path.join(self.temp_dir, "foto.jpg")
        ruta_heic = os.path.join(self.temp_dir, "foto.heic")
        ruta_mp4 = os.path.join(self.temp_dir, "video.mp4")
        ruta_mkv = os.path.join(self.temp_dir, "video.mkv")
        ruta_wav = os.path.join(self.temp_dir, "audio.wav")
        ruta_txt = os.path.join(self.temp_dir, "archivo.txt")

        for r in [ruta_jpg, ruta_heic, ruta_mp4, ruta_mkv, ruta_wav, ruta_txt]:
            with open(r, "wb") as f:
                f.write(b"dummy content")

        self.assertEqual(detectar_tipo_archivo(ruta_jpg), TIPO_IMAGEN_EXIF)
        self.assertEqual(detectar_tipo_archivo(ruta_heic), TIPO_IMAGEN_HEIC)
        self.assertEqual(detectar_tipo_archivo(ruta_mp4), TIPO_VIDEO_MUTAGEN)
        self.assertEqual(detectar_tipo_archivo(ruta_mkv), TIPO_VIDEO_HACHOIR)
        self.assertEqual(detectar_tipo_archivo(ruta_wav), TIPO_AUDIO_WAV)
        self.assertEqual(detectar_tipo_archivo(ruta_txt), TIPO_DESCONOCIDO)

    def test_extraer_metadatos_imagen_con_exif_completo(self):
        """Valida la extracción de fecha y hora en imagen JPEG con EXIF válido."""
        ruta_jpg = os.path.join(self.temp_dir, "prueba_exif.jpg")
        img = Image.new("RGB", (10, 10), color="blue")

        # Guardar con metadatos EXIF simulados usando Pillow Exif
        exif = img.getexif()
        # 36867 es el tag DateTimeOriginal en EXIF
        # 306 es DateTime
        exif[306] = "2023:08:15 14:30:25"
        img.save(ruta_jpg, "jpeg", exif=exif)

        fecha, hora = extraer_metadatos_fecha_hora(ruta_jpg)
        self.assertEqual(fecha, "2023-08-15")
        self.assertEqual(hora, "14-30-25")

    def test_extraer_metadatos_imagen_sin_exif(self):
        """Valida que una imagen sin metadatos retorne (None, None)."""
        ruta_jpg = os.path.join(self.temp_dir, "sin_exif.jpg")
        img = Image.new("RGB", (10, 10), color="red")
        img.save(ruta_jpg, "jpeg")

        fecha, hora = extraer_metadatos_fecha_hora(ruta_jpg)
        self.assertIsNone(fecha)
        self.assertIsNone(hora)

    def test_extraer_metadatos_archivo_inexistente(self):
        """Valida que no lance excepción ante archivo inexistente o corrupto."""
        fecha, hora = extraer_metadatos_fecha_hora(os.path.join(self.temp_dir, "fantasma.jpg"))
        self.assertIsNone(fecha)
        self.assertIsNone(hora)


if __name__ == "__main__":
    unittest.main()
