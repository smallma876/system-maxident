from model.database import get_connection

class Productos:
    def __init__(self,codigo, nombre, idcategoria, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.idcategoria = idcategoria
        self.precio = precio
        self.stock = stock


    @staticmethod
    def search_by_name(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre, idcategoria, precio, stock FROM producto WHERE nombre LIKE ?", ('%' + nombre + '%',))
        
        rows = cursor.fetchall()  # Obtener todas las filas que coincidan
        conn.close()
        
        return [Productos(*row) for row in rows] if rows else []  # Devolver una lista de productos


    
    @staticmethod
    def fetch_all():
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM producto")
                    return cursor.fetchall()  # Asegúrate de devolver todos los registros
        except Exception as e:
            print(f"Ocurrió un error al recuperar productos: {str(e)}")
            return []



    @staticmethod
    def create(nombre, idcategoria, precio, stock):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO producto (nombre, idcategoria, precio, stock) VALUES (?, ?, ?, ?)",
                       (nombre, idcategoria, precio, stock))
        conn.commit()
        conn.close()

    @staticmethod
    def update(codigo, nombre, idcategoria, precio, stock):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE producto SET nombre = ?, idcategoria = ?, precio = ?, stock = ? WHERE codigo = ?",
                    (nombre,idcategoria, precio, stock,codigo))
        conn.commit()
        conn.close()

    @staticmethod
    def search(codigo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre,idcategoria, precio, stock FROM producto WHERE codigo = ?", (codigo,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Productos(*row)
        return None
    
    @staticmethod
    def get_codigo_by_nombre(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo FROM producto WHERE nombre = ?", (nombre,))
        codigo_producto = cursor.fetchone()  # Obtener un solo resultado
        conn.close()
        return codigo_producto[0] if codigo_producto else None  # Devuelve el código o None si no existe
    

    #def delete(codigo):
        #conn = get_connection()
        #cursor = conn.cursor()
        #cursor.execute("DELETE FROM producto WHERE codigo = ?", (codigo,))
        #conn.commit()
        #conn.close()

    
  