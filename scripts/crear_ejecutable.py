import os
import subprocess
import sys

def crear_ejecutable():
    """Crea un ejecutable .exe del programa usando PyInstaller."""
    try:
        # Instalar PyInstaller si no está instalado
        print("Verificando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Obtener rutas del proyecto
        script_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(script_dir)
        
        # Usar rutas absolutas para build y dist en el directorio raíz del proyecto
        work_path = os.path.join(project_dir, 'build')
        dist_path = os.path.join(project_dir, 'dist')
        spec_file = os.path.join(project_dir, 'renombrarfotos.spec')
        
        # Verificar que el spec file existe
        if not os.path.exists(spec_file):
            print(f"ERROR: No se encuentra el archivo {spec_file}")
            print("El archivo de configuración .spec es necesario para la compilación.")
            input("\nPresione Enter para salir...")
            return
        
        print(f"\nUsando configuración: {spec_file}")
        print("Compilando...")
        print("=" * 60)
        
        # Limpiar directorios build y dist antes de compilar
        print("Limpiando directorios temporales...")
        import shutil
        for dir_path in [work_path, dist_path]:
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"✓ Limpiado: {dir_path}")
                except Exception as e:
                    print(f"⚠ No se pudo limpiar {dir_path}: {e}")
            else:
                print(f"✓ Directorio no existe: {dir_path}")
        
        # Compilar usando el spec file pre-configurado
        # --clean asegura una compilación limpia
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller",
            spec_file,
            "--clean",
            "--workpath", work_path,
            "--distpath", dist_path
        ])
        
        exe_path = os.path.join(dist_path, 'RenombrarFotos.exe')
        
        print("\n" + "=" * 60)
        print("✓ Ejecutable creado exitosamente!")
        print(f"✓ Ubicación: {exe_path}")
        print("=" * 60)
        
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ Tamaño: {size_mb:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error durante la compilación.")
        print(f"Código de salida: {e.returncode}")
    except Exception as e:
        print(f"\n✗ Error al crear el ejecutable: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    crear_ejecutable()
 