# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 21:27:37 2017

@author: David Roberts
"""

import psycopg2
from configparser import ConfigParser
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
    
def upsert_batch_id(batch_id):
    """
    Checks for batch id in batches table
    If not exists, create new batch row
    """
    
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute('INSERT INTO dev.batchs (id) VALUES ({}) ON CONFLICT DO NOTHING'.format(batch_id))
        conn.commit()
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    
def write_db_row(batch_id, row_dict):

    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print("Inserting row -- ", row_dict)
        cur.execute(build_sensor_reading_sql(batch_id, row_dict))
        conn.commit()
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            
def build_sensor_reading_sql(batch_id, row_dict):
    

    batch_id = batch_id
    created_at = row_dict['timestamp']
    pH = row_dict['pH']
    temp_f = row_dict['temp_f']
    temp_c = row_dict['temp_c']

    sql_string = """
                    INSERT INTO dev.measurements
                        (
                        b_id,
                        created_at,
                        pH,
                        temp_f,
                        temp_c
                        )
                    VALUES
                        (
                        {},
                        '{}',
                        {},
                        {},
                        {}                        
                        )
                """.format(batch_id, created_at, pH, temp_f, temp_c)
        
    return sql_string
 
#if __name__ == '__main__':
#    row_dict = {"timestamp": '2017-08-28 21:26:56', 'pH': 1.23, 'temp_f': 42.23, 'temp_c':12.23}
#    write_db_row(1, row_dict)
#    upsert_batch_id(1)