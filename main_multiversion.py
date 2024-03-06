import os
import sys
import time
import shutil
from utils import optimizado, vaciar_carpeta, borrar_si_existe_archivo, borrar_si_existe_carpeta, control_tiempo

def main(nombreAtributo):
    '''Crea las carpetas de la libreria en un .zip listo para subir a AWS.'''
    start_time = time.time()
    # Ejecutar en modo optimizado, es que borra los contenedores.
    optimo, carp_lib = optimizado()

    # Ruta versiones Capa Lambda
    destination_path = "./archivosCapaLambda/python/lib"
    # Crea el directorio si no existe
    os.system(f"mkdir -p {destination_path}")

    # Lista de directorios que contienen los docker-compose.yml
    directories = ["./lambdaPython3.8", "./lambdaPython3.9", "./lambdaPython3.10", "./lambdaPython3.11", "./lambdaPython3.12"]

    # Crea directorios versiones python para la capa lambda sino existen
    for d in directories:
        os.system(f"mkdir -p {destination_path}/{d.replace('./lambdaP','p')}/site-packages/")
        # Borramos si contiene archivos
        vaciar_carpeta(f"{destination_path}/{d.replace('./lambdaP','p')}/site-packages")
    
    # Crea el directorio si no existe y vacia carpeta versiones donde se almacenan los .zip separados
    os.system(f"mkdir -p ./archivosCapaLambda/versiones")
    vaciar_carpeta('./archivosCapaLambda/versiones')

    # Borrar .zip multiversion
    borrar_si_existe_archivo("./archivosCapaLambda/python.zip")

    # Borrando imagenes docker si optimizado es True
    if optimo:
        for d in directories:
            os.system(f"docker rmi {d.replace('./','').replace('.','').lower()}_lambda -f")
        # Limpiando cache
        os.system("docker system prune -f")

    for dir in directories:
        # Navega al directorio
        os.chdir(dir)
        # Levanta el contenedor
        print(f"Levantando contenedor {dir.replace('./l','l')}")
        os.system("docker-compose up -d")
        # Ejecuta el script dentro del contenedor
        print(f'    - Ejecutando script started.')
        os.system(f"docker-compose exec lambda python3 started.py {nombreAtributo}")
        # Cierra y elimina el contenedor
        print(f'    - Cerrando contenedor.')
        os.system("docker-compose down -v")        
        # Comprimir a zip en comprimidos
        os.chdir("./app")
        os.system(f'zip -r9 ./comprimidos/python.zip ./python')
        os.chdir("..")
        # Cambiar nombre carpeta python
        shutil.move('./app/python', f'./app/{nombreAtributo}')
        # Copia la carpeta deseada al host
        print(f'    - Copiando archivos.')
        os.system(f"cp -R ./app/{nombreAtributo}/ .{destination_path}/{dir.replace('./lambdaP','p')}/site-packages/")
        # Borrar carpetas
        print(f"    - Borrando carpetas y .zip de los contenedores.")
        shutil.rmtree(f'./app/{nombreAtributo}')
        # Asegurarse de que la carpeta de destino existe
        os.makedirs(f"../archivosCapaLambda/versiones/{dir.replace('./lambdaP','p')}", exist_ok=True)
        # Ahora puedes mover el archivo de forma segura
        shutil.move('./app/comprimidos/python.zip', f"../archivosCapaLambda/versiones/{dir.replace('./lambdaP','p')}")
        # Regresa al directorio principal
        os.chdir("..")

    # Comprime las carpetas copiadas en un archivo ZIP
    print(f'    - Comprimiendo .zip para capa.')
    os.chdir("./archivosCapaLambda")
    os.system(f"zip -r ./python.zip ./python")

    # Borrando carpetas de versiones y imagen docker si optimizado es True
    print('Limpiando carpetas /python/lib/versiones.. y borrando contenedores.')
    for d in directories:
        vaciar_carpeta(f"./python/lib/{d.replace('./lambdaP','p')}/site-packages")
        if optimo:
            os.system(f"docker rmi {d.replace('./','').replace('.','').lower()}_lambda -f")
    
    # Limpiando cache si optimizado es True
    if optimo:
        os.system("docker system prune -f")

    # Borrando si existe __pycache__
    pycache = f'../__pycache__'
    borrar_si_existe_carpeta(pycache)

    ## Finalizando y limpiando:
    ## Borrar carpeta python para limpiar y crear carpeta libreria para los .zip
    shutil.rmtree('./python')
    if carp_lib:
        if os.path.exists(f'./{nombreAtributo}'):
            shutil.rmtree(f'./{nombreAtributo}')
        else:
            os.mkdir(nombreAtributo)
        shutil.move('./versiones', f'{nombreAtributo}/versiones')
        shutil.move('./python.zip', f'{nombreAtributo}/python.zip')

    end_time = control_tiempo(start_time)
    print(f"""\n\n----- Proceso completado -----
Ya están listos los archivos .zip para crear la capa lambda en aws.
El primer .zip es el multiversión y en la carpeta están separados por versiones.
*Más info de como subir el .zip en el README.

{end_time}

""")


# Ejecución (con o sin argumentos)
'''Ejecutando el script y nombre libreria, por ejemplo: python3 main_multiversion.py psycopg2-binary'''
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Por favor, especifica el nombre de la librería como argumento.")
