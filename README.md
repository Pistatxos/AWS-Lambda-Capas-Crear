# Crear librerías Python para AWS Lambda

**¿Necesitas una libreria python en una lambda de aws?**
Este repositorio proporciona una solución eficiente y accesible para gestionar librerías Python en capas Lambda de AWS. Facilita la creación de capas Lambda personalizadas en diversas versiones de Python mediante el uso de Docker. Siguiendo las mejores prácticas, todo el código está comentado y utiliza contenedores Docker que emulan el sistema Lambda para cada versión de Python, asegurando una compatibilidad óptima y una implementación sencilla. Esto lo hace práctico y útil para cualquiera que desee crear funciones Lambda de manera fácil. Aprenderás a preparar archivos .zip con las librerías necesarias que luego podrás añadir fácilmente a tus funciones Lambda en AWS, simplificando el proceso de desarrollo y despliegue de tus proyectos en la nube.

## ¿Que necesitamos?
Se ha probado desde macOS y Linux. Para windows ya llegará, leer en FAQ. 
Para utilizar este script, asegúrate de tener instalados:
- docker
- docker-compose
- python

### Uso rápido:
Ejecuta el script "main_multiversion.py" y nombre de la librería a descargar, por ejemplo:
`python3 main_multiversion.py psycopg2-binary`

Los archivos .zip estarán en la carpeta "/archivosCapaLambda" donde encontrarás en raiz el que contiene todas las versiones y en las carpetas los archivos separados.
Para más info, continúa ;)

Para tener más información de las capas lambda en aws puedes entrar en:
https://tomonota.net/aws-lambda-capas-layers

## Crear libreria multi-versiones
Para preparar una librería compatible con múltiples versiones de Python, sigue estos pasos desde la carpeta raíz del proyecto:
- `python3 main_multiversion.py <nombre_de_la_librería>`

Por ejemplo:
- `python3 main_multiversion.py psycopg2-binary`

Este comando descargará y preparará las versiones de la librería seleccionada dentro de la carpeta `/archivoCapaZip/versiones`, generando además un archivo `python.zip` que incluye todas las versiones, listo para subir como capa Lambda en AWS. Existe la posibilidad de cambiarlo en el config.py (leer más abajo).

## Crear libreria de una versión en concreto
Si deseas crear una librería para una versión específica de Python, navega a la carpeta correspondiente (por ejemplo, `/lambdaPython3.9`) y ejecuta:
- `python3 main.py <nombre_de_la_librería>`

Por ejemplo:
- `python3 main.py psycopg2-binary`

El script descargará y preparará la librería dentro de `/app/nombreLibreria`, y almacenará el archivo .zip listo para usar como capa Lambda en `/app/comprimidos`.

## Opciones de configuración:
En el script `config.py` están las variables de configuración:
#### "optimizado"
- `True`: El script creará y eliminará los contenedores de Docker en cada ejecución, sin almacenar datos innecesariamente.
- `False`: Los contenedores se detendrán pero no se eliminarán, lo que permite reutilizarlos para ejecuciones subsiguientes y ahorrar tiempo. Se recomienda activar esta opción solo en la última ejecución para limpiar imágenes y caché.
#### "carpeta_libreria"
- `True`: El script al finalizar creará una carpeta con el nombre de la librería descargada y añadirá la carpeta de versiones y el archivo .zip multiversión.
- `False`: Dejará las carpetas por defecto de versiones y el archivo.zip en la carpeta de archivosCapaLabda sustituyéndose en cada ejecución.


# Añadir Capa Lambda AWS.
Para crear una capa en Lambda:

1. En la consola de AWS Lambda ve al menú de Capas.
2. Crear una nueva capa. Añade un nombre, selecciona las arquitecturas, los tiempos de ejecución, la versión de python y carga el `python.zip` de dicha versión.
3. Seguidamente, desde la función de lambda ya puedes hacer el import.

## Crear Capa Lambda Multi-versiones en AWS
El proceso para crear una capa que soporte múltiples versiones de Python es similar al anterior, asegurándote de seleccionar todas las versiones de Python soportadas durante la creación de la capa.

Siguiendo estos pasos, podrás gestionar eficientemente las librerías Python para tus proyectos en AWS Lambda, maximizando la compatibilidad y rendimiento de tus funciones.


# FAQ

**¿Te gusta este proyecto y te ha sido útil?**  
Dale una estrella para animarme a seguir actualizando la repo.

**¿Sería posible hacer todo en un solo Dockerfile?**  
Sí, es posible. Sin embargo, he creado el script para manejarlo por versiones. En algunas ocasiones, las bibliotecas ocupan demasiado espacio y no es posible crear una imagen multiversión debido a que las capas de Docker tienen un límite de MB. Para optimizar el uso del espacio se recomienda crear capas por versiones. Aunque, en el caso de librerías más ligeras, como `psycopg2-binary`, es posible crear una sola capa que sirva para todas las versiones.

**Próximas actualizaciones**
- Ejecutar desde windows:
    Poder ejecutar desde windows el proceso para todos aquellos que lo necesiten. En principio habrá que revisar rutas y el proceso de comprimir ;) Se irá viendo.