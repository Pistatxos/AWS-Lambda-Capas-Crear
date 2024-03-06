import os
import sys
import shutil

def optimizado():
    if os.path.exists("config.py"):
        from config import optimizado
        resp = optimizado
    else:
        with open('config.py', 'w') as b:
            b.write('optimizado = True')
        resp = True
    return resp

def main(nombreAtributo):
    # Si optimizado es True
    optimo = optimizado()

    # Navega al directorio
    os.chdir('./app')
    nombre_carpeta = os.path.basename(os.getcwd())

    # Levanta el contenedor
    print(f"Levantando contenedor {nombre_carpeta}")
    os.system("docker-compose up -d")

    # Ejecuta el script dentro del contenedor
    print(f'    - Ejecutando script started.')
    os.system(f"docker-compose exec lambda python3 started.py {nombreAtributo}")

    # Cierra y elimina el contenedor
    print(f'    - Cerrando contenedor.')
    os.system("docker-compose down -v")        

    # Comprimir carpeta libreria a zip en /comprimidos
    os.system(f'zip -r9 ./comprimidos/python.zip ./python')

    # Cambiar nombre carpeta python
    shutil.move('./python', f'./{nombreAtributo}')

    # Saliendo ruta
    os.chdir("..")

    if optimo:
        # Borrando imagen docker
        os.system(f"docker rmi {nombre_carpeta.replace('.','').lower()}_lambda -f")
        # Limpiando cache
        os.system("docker system prune -f")

    # Borrando si existe __pycache__
    pycache = f'./__pycache__'
    if os.path.exists(pycache):
        # Intentar eliminar la carpeta
        try:
            shutil.rmtree(pycache)
        except Exception as e:
            print(f"Error al eliminar __pycache__: {e}")
    else:
        pass

    # Confirmación
    print('Archivo python.zip preparado para subir a la capa lambda de aws.')
    print('Ya puedes cerrar el contendor!')


# Ejecución
if __name__ == '__main__':
    # Si existen argumentos
    if len(sys.argv) > 1:
        main(sys.argv[1])
    # Si no existen argumentos
    else:
        print("Por favor, especifica el nombre de la librería como argumento.")
