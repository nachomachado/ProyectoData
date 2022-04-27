import requests
import pandas as pd
import requests
import csv
import io
import os
import datetime


def normalize(s):
    """
    Reemplaza los caracteres con tilde por caracteres sin tilde.
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


def columns_to_lower(df):
    """
    Pasa a minisculas los caracteres
    """
    lower_name = []
    for name in df.columns:
        lower_name.append(normalize(name.lower()))
    return lower_name


def mkdirs(files):
    """
    Esta fucion es la encargada de guardar los .csv descargados de las URLs en los directorios
    siguiendo el siguiente formato:
    categoría\año-mes\categoria-dia-mes-año.csv
    """
    today = datetime.date.today()
    ano_mes = today.strftime("%Y-%B")
    d_m_a = today.strftime("-%d-%m-%Y")
    for c in files.keys():
        if not os.path.exists(os.path.join(c)):
            path = os.path.join(c)
            os.makedirs(path)
        else:
            pass
        if not os.path.exists(os.path.join(c, ano_mes)):
            path = os.path.join(c, ano_mes)
            os.makedirs(path)
        else:
            pass
        if not os.path.exists(os.path.join(c, ano_mes, c + d_m_a)):
            path = os.path.join(c, ano_mes, c + d_m_a)
            os.makedirs(path)
        else:
            pass
        path = os.path.join(c, ano_mes, c + d_m_a)
        files[c].to_csv(os.path.join(path, c+'.csv'))
    return


def run():
    """
    Este modulo es el encargado de descargar los datos de las URLs y realizar el 
    procesamiento de los datos. Luego los almacenas en archivos .csv para finalmente
    ser actualizados en la DB.
    """
    # Se guaran el las URLs donde se van a solicitar los datos
    url_bibliotecas = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv'
    url_cines = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv'
    url_museos = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv'
    response_bibliotecas = requests.get(url_bibliotecas).content
    response_cines = requests.get(url_cines).content
    response_museos = requests.get(url_museos).content
    # Se almacena cada tabla en un DataFrame para su procesamiento con Pandas
    bibliotecas = pd.read_csv(io.StringIO(response_bibliotecas.decode('utf-8')))
    cines = pd.read_csv(io.StringIO(response_cines.decode('utf-8')))
    museos = pd.read_csv(io.StringIO(response_museos.decode('utf-8')))
    # Se pasan a minisculas 
    cines.columns = columns_to_lower(cines)
    museos.columns = columns_to_lower(museos)
    bibliotecas.columns = columns_to_lower(bibliotecas)
    # Se cambia el nombre de la columna para tener consistencia
    bibliotecas.rename(columns={'domicilio': 'direccion'}, inplace=True)
    # Se definen las columnas que van a ser necesarias para la tabla normalizada
    need_columns = [
        'cod_loc',
        'idprovincia',
        'iddepartamento',
        'categoria',
        'provincia',
        'localidad',
        'nombre',
        'direccion',
        'cp',
        'telefono',
        'mail',
        'web',
        'fuente']
    # Se concatenan datos para crear la tabla normalizada
    data = pd.concat([
        museos[need_columns], 
        cines[need_columns], 
        bibliotecas[need_columns]], 
        ignore_index=True)
    # En la exploracion de datos se observa que la provincia Salta posee mas de un id, por lo que se normalizan a uno solo. ID = 66.
    salta_mask = data.provincia == 'Salta'
    data.loc[salta_mask, 'idprovincia'] = data[salta_mask]['idprovincia'].map({58: 66, 66: 66})
    # En la exploracion se observa que Santa Fe se encuentra con tile y sin Tile por lo que se corrige
    sfe_mask = data.provincia == 'Santa Fé'
    data.loc[sfe_mask, 'provincia'] = data[sfe_mask]['provincia'].map({'Santa Fé': 'Santa Fe'})
    # Se corrigen nombres de provincias
    data.loc[data.idprovincia == 58, 'provincia'] = 'Neuquén'
    data.loc[data.idprovincia == 94, 'provincia'] = 'Tierra del Fuego, Antártida e Islas del Atlántico Sur'
    # Se renombran columnas para que se encuentren segun enunciado
    data = data.rename(columns={
        'cod_loc': 'cod_localidad', 
        'idprovincia': 'id_provincia', 
        'iddepartamento': 'id_departamento', 
        'direccion': 'domicilio'})
    # Se crean las tablas en funcion de aca enunciado 
    reg_cat = data.groupby('fuente')['fuente'].count().to_frame().rename(columns={'fuente': 'cantidad'}).reset_index()
    reg_fuente = data.groupby('fuente')['fuente'].count().to_frame().rename(columns={'fuente': 'cantidad'}).reset_index()
    reg_prov_cat = data.groupby(['provincia', 'categoria'])['categoria'].count().to_frame().rename(columns={'categoria': 'cantidad'}).reset_index()
    cat_but_pant_espa = cines.groupby('provincia')[['pantallas', 'butacas', 'espacio_incaa']].count().reset_index()
    # Se guardan los df procesados en los .csv para luego cargarlos en la DB
    data.to_csv('data.csv')
    reg_cat.to_csv('reg_cat.csv')
    reg_fuente.to_csv('reg_fuente.csv')
    reg_prov_cat.to_csv('reg_prov_cat.csv')
    cat_but_pant_espa.to_csv('cat_but_pant_espa.csv')
    # Se crea este diccionario para definir las categorias y las tablas en cada categoria
    categorias = {'cines': cines, 'museos': museos, 'bibliotecas': bibliotecas}
    # Se almacena cada tabla en su directorio en funcion de la categoria
    mkdirs(categorias)
    return


if __name__ == '__main__':
    run()
    print('Done!')
