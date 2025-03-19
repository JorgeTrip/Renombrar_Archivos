import os
import subprocess
import sys

def crear_ejecutable():
    """Crea un ejecutable .exe del programa usando PyInstaller."""
    try:
        # Instalar PyInstaller si no está instalado
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Obtener la ruta del script principal y la raíz del proyecto
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'renombrar', 'main.py')
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # Crear directorios de build si no existen
        build_dir = os.path.join(project_root, 'build')
        dist_dir = os.path.join(project_root, 'dist')
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(dist_dir, exist_ok=True)
        
        # Crear el ejecutable sin ícono
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller",
            "--onefile",
            "--name=RenombrarFotos",
            f"--distpath={dist_dir}",
            f"--workpath={build_dir}",
            f"--specpath={build_dir}",
            script_path
        ])
        
        print("\nEjecutable creado exitosamente!")
        print(f"Puedes encontrar el archivo RenombrarFotos.exe en la carpeta {dist_dir}")
        
        # Limpiar archivos temporales
        spec_file = os.path.join(build_dir, 'RenombrarFotos.spec')
        if os.path.exists(spec_file):
            os.remove(spec_file)
        
    except Exception as e:
        print(f"Error al crear el ejecutable: {e}")
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    crear_ejecutable() 