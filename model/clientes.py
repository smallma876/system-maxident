from model.database import get_connection

class Clientes:
    def __init__(self, idcliente, nombre, telefono, direccion, agencia_entrega, ruc_dni,forma_entrega):
        self.idcliente = idcliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.agencia_entrega = agencia_entrega
        self.ruc_dni = ruc_dni
        self.forma_entrega = forma_entrega

    @staticmethod
    def search_by_name(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idcliente, nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega FROM clientes WHERE nombre LIKE ?", ('%' + nombre + '%',))
        
        rows = cursor.fetchall()  # Obtener todas las filas que coincidan
        conn.close()
        
        return [Clientes(*row) for row in rows] if rows else []  # Devolver una lista de clientes

    @staticmethod
    def fetch_all():
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM clientes")
                    return cursor.fetchall()  # Asegúrate de devolver todos los registros
        except Exception as e:
            print(f"Ocurrió un error al recuperar clientes: {str(e)}")
            return []

    @staticmethod
    def create(nombre, telefono, direccion, agencia_entrega,ruc_dni, forma_entrega):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega) VALUES (?, ?, ?, ?, ?,?)",
                       (nombre, telefono, direccion, agencia_entrega,ruc_dni, forma_entrega))
        conn.commit()
        conn.close()

    @staticmethod
    def update(idcliente, nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET nombre = ?, telefono = ?, direccion = ?, agencia_entrega = ?, ruc_dni = ? , forma_entrega = ? WHERE idcliente = ?",
                       (nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega, idcliente))
        conn.commit()
        conn.close()

    @staticmethod
    def search(idcliente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idcliente, nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega FROM clientes WHERE idcliente = ?", (idcliente,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Clientes(*row)
        return None


    @staticmethod
    def get_ruc_dni(cliente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ruc_dni FROM clientes WHERE nombre = ?", (cliente,))
        ruc_dni = cursor.fetchone()  # Suponiendo que solo hay un cliente por nombre
        conn.close()
        return ruc_dni[0] if ruc_dni else None  # Devuelve el RUC o DNI si existe
    
    @staticmethod
    def get_id_by_nombre(nombre):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idcliente FROM clientes WHERE nombre = ?", (nombre,))
        id_cliente = cursor.fetchone()  # Obtener un solo resultado
        conn.close()
        return id_cliente[0] if id_cliente else None  # Devuelve el ID o None si no existe