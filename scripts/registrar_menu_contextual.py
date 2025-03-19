import os
import sys
import winreg
import subprocess

def registrar_menu_contextual():
    """Registra el comando 'Renombrar archivos de fotos' en el menú contextual de Windows."""
    try:
        # Obtener la ruta del ejecutable de Python
        python_path = sys.executable
        
        # Obtener la ruta del script principal
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'renombrar', 'main.py')
        
        # Crear el comando que se ejecutará
        comando = f'"{python_path}" "{script_path}"'
        
        # Registrar en el menú contextual de carpetas
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell\RenombrarFotos") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Renombrar archivos de fotos")
            winreg.SetValue(key, "Icon", winreg.REG_SZ, "shell32.dll,147")
            
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell\RenombrarFotos\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, comando)
            
        # Registrar también para carpetas individuales
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\RenombrarFotos") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Renombrar archivos de fotos")
            winreg.SetValue(key, "Icon", winreg.REG_SZ, "shell32.dll,147")
            
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\RenombrarFotos\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, comando)
            
        print("Menú contextual registrado exitosamente!")
        print("Ahora puedes hacer clic derecho en cualquier carpeta y verás la opción 'Renombrar archivos de fotos'")
        
    except Exception as e:
        print(f"Error al registrar el menú contextual: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    registrar_menu_contextual() 