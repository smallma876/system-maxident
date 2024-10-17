#El Modelo se encarga de manejar los datos y la lógica de negocio de la aplicación. Es responsable de acceder a la base de datos, 
# realizar cálculos y aplicar reglas de negocio. En Python, el Modelo podría ser una clase que define la estructura de los datos y 
# contiene métodos para manipular esos datos.

import pyodbc
def get_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-2GU3A1F\\SQLEXPRESS;'
        'DATABASE=MAX&DENT;'
        'Trusted_Connection=yes;'
    )
    return connection