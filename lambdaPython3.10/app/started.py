import os
import shutil
import sys
import time

def ejecutar(comando):
    # Ejecutar comando de terminal
    os.system(comando)

def main(libreria):
    # Crear carpeta para los comprimidos si no existe
    if not os.path.exists('./comprimidos'):
        os.makedirs('./comprimidos')
    # variables archivo .zip y carpetas descarga
    archivo_a_eliminar = './comprimidos/python.zip'
    carpeta_a_eliminar = f'./{libreria}'
    carpeta_python = './comprimidos/python'

    # Borrando .zip si existe
    if os.path.exists(archivo_a_eliminar):
        # Intentar eliminar la carpeta
        try:
            os.remove(archivo_a_eliminar)
            print(f"El archivo '{archivo_a_eliminar}' ha sido eliminado..")
        except Exception as e:
            print(f"Error al eliminar el archivo '{archivo_a_eliminar}': {e}")
    else:
        pass
    # Borrando libreria si existe
    if os.path.exists(carpeta_a_eliminar):
        # Intentar eliminar la carpeta
        try:
            shutil.rmtree(carpeta_a_eliminar)
            print(f"La carpeta '{carpeta_a_eliminar}' ha sido eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la carpeta '{carpeta_a_eliminar}': {e}")
    else:
        pass
    # Borrando carpeta python si existe
    if os.path.exists(carpeta_python):
        # Intentar eliminar la carpeta
        try:
            shutil.rmtree(carpeta_python)
            print(f"La carpeta '{carpeta_python}' ha sido eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la carpeta '{carpeta_python}': {e}")
    else:
        pass

    # Instalando pip
    ejecutar(f'pip install {libreria} -t ./python')

    time.sleep(5)

    # Borrando si existe __pycache__
    pycache = f'./python/__pycache__'
    if os.path.exists(pycache):
        # Intentar eliminar la carpeta
        try:
            shutil.rmtree(pycache)
            print(f"Eliminada __pycache__ de la carpeta de la libreria.")
        except Exception as e:
            print(f"Error al eliminar __pycache__: {e}")
    else:
        pass

# Ejecución
if __name__ == '__main__':
    # Si existen argumentos
    if len(sys.argv) > 1:
        main(sys.argv[1])
    # Si no existen argumentos
    else:
        print("Por favor, especifica el nombre de la librería como argumento.")
