from model.database import get_connection

class Cotizaciones:
    def __init__(self, id, idcliente, fecha, codigo, cantidad, precio_unitario, total, estado):
        self.id = id 
        self.idcliente = idcliente
        self.fecha = fecha
        self.codigo = codigo
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total
        self.estado = estado
        

    @staticmethod
    def create(idcliente, fecha, codigo, cantidad, precio_unitario, total, estado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cotizaciones (idcliente, fecha, codigo, cantidad, precio_unitario, total, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (idcliente, fecha, codigo, cantidad, precio_unitario, total, estado, ))
        conn.commit()
        conn.close()
    
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
    def search_by_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cotizaciones WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cotizaciones(*row)
        return None

    @staticmethod
    def update_estado(id, estado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cotizaciones SET estado = ? WHERE id = ?", (estado, id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cotizaciones WHERE id = ?", (id,))
        conn.commit()
        conn.close()