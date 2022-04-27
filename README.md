# Desarrollo de Challenge Alkemy
Este proyecto trata sobre el desarrollo del challenge de Alkemy.
## Contenido
El proyecto contiene los siguientes archivos:
- _database.ini_: Es el archivo de configuración y conexión a la base de datos PostgresSQL dónde se almacenarán las datos procesados. 
- Archivos _.sql_ para la creacion de las tablas:
    1. 1_data.sql: Script que crea la tabla que resume todos los datos procesados, de todas las categorias, todas las provincias y todas las fuentes. Esta es la tabla nomalizada.
    2. 2_reg_cat.sql: Script que crea la tabla de **Cantidad de registros totales por categoría**.
    3. 3_reg_fuen.sql: Script que crea la tabla de **Cantidad de registros totales por fuente**.
    4. 4_reg_prov_cat.sql: Script que crea la tabla de **Cantidad de registros por provincia y categoría**.
    5. 5_cant_pant_buta_espa.sql: Script que crea la tabla de la tabla contiene la informacion de **Provincia**, **Cantidad de pantallas**, **Cantidad de butacas** y **Cantidad de espacios INCAA**. 
- Modulos de python _.py_: Todos éstos módulos poseen una función `run()` que ejecuta el contenido principal.
    1. _procesamiento.py_: Éste módulo obtiene los datos de las URLs brindadas:
    
       - [Datos Argentina - Museos](https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d)
       - [Datos Argentina - Salas de Cine](https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae)
       - [Datos Argentina - Bibliotecas Populares](https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7)
   
        Luego los almacena en DataFrames y realiza las modificaciones para mejorar la consistencia de los datos según lo observado en la exploración realizada en el archivo jupyter notebook _Challenge.ipynb_. Posteriormente crea las tablas requeridas por el challenge y las almacena en archivos _.csv_. Por último, crea los directorios según el formato especificado y almacena las 3 tablas originales obtenidas de los URLs. 
    2. _database.py_: Éste módulo crea la DB según la configuración almacenada en el archivo _database.ini_ y ejecuta los 5 scripts _.sql_ que crean las tablas dónde se almacenarán los datos procesados. Éste módulo es el que posee las funciones de conexión a la base de datos utilizando la librería SQLalchemy.
    3. _main.py_: Éste módulo ejecuta los dos módulos anteriormente mencionados. Luego actualiza los datos requeridos guardados en los _.csv_ generados por el módulo _preprocesamiento.py_ en las tablas creadas por los scripts _.sql_ (dichas tablas fueron las creadas en el módulo _database.py_).
- _Challenge.ipynb_: Jupyter Notebook dónde se realiza parte del procesamiento y visualización para el entendimiento del dataset y verificar la consistencia de los datos.
- _Challenge Data Analytics con Python.pdf_: Enunciado y requerimentos del challenge. 
- _requirements.txt_: Paquetes para ser instalados en el ambiente de python para correr el proyecto. 
## Configuración
El archivo de configuración es el _database.ini_. En él se pueden encontrar los datos para el acceso y configuración a la base de datos. En caso de querer hacer el deploy en una base de datos especifica se deben modificar los datos de acceso a la misma teniendo la siguiente estructura:

> [postgresql]
> 
> host=localhost
>
> database=challenge
> 
> user=postgres
> 
> password=postgres
> 
> port=5432

Por default se encuentran los datos de acceso predeterminados de PostgresSQL.
## Uso
Se debe ejecutar desde la terminal el módulo _main.py_ en el ambiente que posee instalados todos los paquetes nombrados en _requirementes.txt_. Al finalizar la ejecución se observarán las carpetas creadas con las 3 tablas originales y los archivos creados en la raiz del proyecto. También se encontrarán actualizados los datos en la DB configurada y un mensaje `Done!` en terminal.
## Contacto
- Autor: **Ignacio Machado**
- Mail: **ignmachado@gmail.com**