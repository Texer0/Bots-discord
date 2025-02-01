import sqlite3

def try_query(sql, params=()):
    try:
        conexion = sqlite3.connect('sanciones.db')
        cursor = conexion.cursor()
        
        cursor.execute(sql, params)
        
        if sql.strip().upper().startswith("SELECT"):
            resultado = cursor.fetchall()
            return resultado[0] if resultado else []
        
        conexion.commit()
        print("Query ejecutada correctamente.")
        return None
    
    except sqlite3.Error as error:
        print("Error al ejecutar la query:", error)
        return None
    
    finally:
        conexion.close()

    
def select_query(table, columns, condition= None):
    if not condition:
        query = f"SELECT {columns} FROM {table};"
    else:
        query = f"SELECT {columns} FROM {table} WHERE {condition};"
    return try_query(query)


def insert_into_query(table, columns, data):
    query = f"INSERT INTO {table} ({columns}) VALUES ({data});"
    return try_query(query)

