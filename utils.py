import os
import time
import shutil

def vaciar_carpeta(carpeta):
    '''Vacia la carpeta de la ruta indicada en el atributo.'''
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        try:
            if os.path.isfile(ruta) or os.path.islink(ruta):
                os.unlink(ruta)  # Para borrar archivos y enlaces simbólicos
            elif os.path.isdir(ruta):
                shutil.rmtree(ruta)  # Para borrar directorios y todo su contenido
        except Exception as e:
            print(f'Error al borrar {ruta}. Razón: {e}')

def optimizado():
    '''Lee la variable optimizado, sino encuentra config.py lo crea con lo necesario en True.'''
    if os.path.exists("config.py"):
        from config import optimizado, carpeta_libreria
        optimo = optimizado
        carp_lib = carpeta_libreria
    else:
        with open('config.py', 'w') as b:
            b.write('optimizado = True\ncarp_lib = False')
        optimo = True
        carp_lib = False
    return optimo, carp_lib

def borrar_si_existe_archivo(ruta_archivo):
    '''Borra archivo si existe.'''
    if os.path.exists(ruta_archivo):
        # Intentar eliminar la carpeta
        try:
            os.remove(ruta_archivo)
            print(f"El archivo {ruta_archivo} se ha borrado para no duplicar.")
        except Exception as e:
            print(f"Error al eliminar el archivo {ruta_archivo}:\n{e}")

def borrar_si_existe_carpeta(ruta_carpeta):
    '''Borra carpeta si existe.'''
    if os.path.exists(ruta_carpeta):
        # Intentar eliminar la carpeta
        try:
            shutil.rmtree(ruta_carpeta)
            print(f"La carpeta {ruta_carpeta} se ha borrado.")
        except Exception as e:
            print(f"Error al eliminar la carpeta {ruta_carpeta}:\n{e}")

def control_tiempo(start_time):
    end_time = time.time()
    total_time = end_time - start_time
    # Calcula minutos y segundos
    minutos = total_time // 60
    segundos = total_time % 60
    tiempo = f"Tiempo total de ejecución: {int(minutos)} minutos y {segundos:.2f} segundos."
    return tiempo
