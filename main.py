from database import load_connection_info
import database
import procesamiento
import sqlalchemy as db
import pandas as pd


def run():

    # Se ejecuta el modulo procesamiento.py
    procesamiento.run()
    # Se ejecuta el modulo database.py
    database.run()
    # Se leen los datos de conexion y se crea el engine de conexion
    conn_info = load_connection_info("database.ini")
    engine = db.create_engine(
        f"postgresql+psycopg2://" +
        f"{conn_info['user']}:" +
        f"{conn_info['password']}@" +
        f"{conn_info['host']}:" +
        f"{conn_info['port']}/{conn_info['database']}")
    # Se conecta a la DB
    connection = engine.connect()
    # Se leen los .csv creados por el modulo procesamiento.py
    data = pd.read_csv('data.csv')
    reg_cat = pd.read_csv('reg_cat.csv')
    reg_fuente = pd.read_csv('reg_fuente.csv')
    reg_prov_cat = pd.read_csv('reg_prov_cat.csv')
    cat_but_pant_espa = pd.read_csv('cat_but_pant_espa.csv')
    # Se actualiza la marca temporal al momento de realizar la actualizacion
    data['fecha_carga'] = pd.Timestamp.now()
    reg_cat['fecha_carga'] = pd.Timestamp.now()
    reg_fuente['fecha_carga'] = pd.Timestamp.now()
    reg_prov_cat['fecha_carga'] = pd.Timestamp.now()
    # Se actualizan datos en cada tabla y si existen se reemplazan
    data.to_sql('data', engine, if_exists='replace', index=False)
    reg_cat.to_sql('reg_cat', engine, if_exists='replace', index=False)
    reg_fuente.to_sql('reg_fuente', engine, if_exists='replace', index=False)
    reg_prov_cat.to_sql('reg_prov_cat', engine, if_exists='replace', index=False)
    cat_but_pant_espa.to_sql('cat_but_pant_espa', engine, if_exists='replace', index=False)
    # Se cierra conexion a la DB
    connection.close()
    print('Done!')
    return


if __name__ == '__main__':
    '''
    Entry point
    '''
    run()

