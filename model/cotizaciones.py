from model.database import get_connection

class Cotizaciones:
    def __init__(self, idcotizaciones, idcliente, fecha, total):
        self.idcotizaciones = idcotizaciones 
        self.idcliente = idcliente
        self.fecha = fecha
        self.total = total
       
    
    @staticmethod
    def create(idcliente, fecha):
        conn = None
        try:
            print("Conectando a la base de datos...")
            conn = get_connection()
            if conn is None:
                raise Exception("No se pudo establecer conexión a la base de datos.")
            
            cursor = conn.cursor()
            print(f"Inserción de cotización: ID Cliente = {idcliente}, Fecha = {fecha}")
            
            # Ejecutar la inserción y recuperar el ID al mismo tiempo
            cursor.execute("INSERT INTO cotizaciones (idcliente, fecha) OUTPUT INSERTED.idcotizaciones VALUES (?, ?)", (idcliente, fecha))
            result = cursor.fetchone()  # Obtener el ID de la inserción
            print(f"Resultado de la inserción: {result}")
            
            conn.commit()  # Realizar el commit después de la inserción

            if result is not None:
                idcotizaciones = result[0]  # Recuperar el primer valor de la tupla
                print(f"Cotización creada con ID: {idcotizaciones}")
                return idcotizaciones
            else:
                print("No se pudo recuperar el ID de la cotización. La inserción puede haber fallado.")
                return None

        except Exception as e:
            print(f"Error al crear la cotización: {e}")
            print("Datos que se intentaron insertar:")
            print(f"ID Cliente: {idcliente}, Fecha: {fecha}")
            return None
        finally:
            if conn:
                conn.close()  # Cerrar la conexión en cualquier caso, éxito o error
                
                
    @staticmethod
    def fetch_clientes():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idcliente, nombre FROM clientes")
        rows = cursor.fetchall()
        conn.close()
        return [row.nombre for row in rows] if rows else []  # Solo devuelve los nombres


    @staticmethod
    def fetch_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cotizaciones")
        rows = cursor.fetchall()
        conn.close()
        return [Cotizaciones(*row) for row in rows] if rows else []

    @staticmethod
    def search_by_id(idcotizaciones):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cotizaciones WHERE id = ?", (idcotizaciones,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cotizaciones(*row)
        return None

    @staticmethod
    def delete(idcotizaciones):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cotizaciones WHERE id = ?", (idcotizaciones,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_total(idcotizaciones, total):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cotizaciones SET total = ? WHERE idcotizaciones = ?", (total, idcotizaciones))
        conn.commit()
        conn.close()