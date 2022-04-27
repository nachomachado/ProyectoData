from configparser import ConfigParser
import psycopg2
from typing import Dict


def load_connection_info(ini_filename):
    """
    Esta funcion toma los datos del archivo .ini y los carga 
    en un diccionario.
    """
    parser = ConfigParser()
    parser.read(ini_filename)
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def create_db(conn_info):
    """
    Funcion que crea la DB. Si ya se encuentra creada, cierra cursor. 
    """
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"
    try:
        cur.execute(sql_query)
    except Exception as e:
        cur.close()
    else:
        conn.autocommit = False


def create_table(sql_query, conn, cur):
    """
    Funcion que ejecuta el query sql para la creacion de las tablas. 
    """
    try:
        cur.execute(sql_query)
    except Exception as e:
        conn.rollback()
        cur.close()
    else:
        conn.commit()


def run():
    # Se cargan host, database, usuario y password
    conn_info = load_connection_info("database.ini")
    create_db(conn_info)
    # Se establece la conexion en funcion del archivo de configuracion
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()
    # Se crea la tabla 1
    tabla_1 = open("1_data.sql")
    tabla_1_string = tabla_1.read()
    create_table(tabla_1_string, connection, cursor)
    # Se crea la tabla 2 
    tabla_2 = open("2_reg_cat.sql")
    tabla_2_string = tabla_2.read()
    cursor = connection.cursor()
    create_table(tabla_2_string, connection, cursor)
    # Se crea la tabla tabla 3
    tabla_3 = open("3_reg_fuen.sql")
    tabla_3_string = tabla_3.read()
    cursor = connection.cursor()
    create_table(tabla_3_string, connection, cursor)
    # Se crea la tabla 4
    tabla_4 = open("4_reg_prov_cat.sql")
    tabla_4_string = tabla_4.read()
    cursor = connection.cursor()
    create_table(tabla_4_string, connection, cursor)
    # Se crea la tabla 5
    tabla_5 = open("5_cant_pant_buta_espa.sql")
    tabla_5_string = tabla_5.read()
    cursor = connection.cursor()
    create_table(tabla_5_string, connection, cursor)
    # Se cierra la conexion
    connection.close()
    cursor.close()
    return

if __name__ == "__main__":
    run()
    print('done!')