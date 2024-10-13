from model.database import get_connection 

class DetalleCotizaciones:
    def __init__(self,id_detalle_cotizaciones, idcotizaciones, codigo, cantidad, precio_unitario):
        self.id_detalle_cotizaciones = id_detalle_cotizaciones
        self.idcotizaciones = idcotizaciones
        self.nombre = codigo
        self.ruc_dni = cantidad
        self.agencia_entrega = precio_unitario
        

    
    @staticmethod
    def create(idcotizaciones, codigo, cantidad, precio_unitario):
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO detalle_cotizaciones (idcotizaciones, codigo, cantidad, precio_unitario) VALUES (?, ?, ?, ?)", 
                (idcotizaciones, codigo, cantidad, precio_unitario,)
            )
            connection.commit()
    
    @staticmethod
    def agregar_detalle_cotizacion(idcotizaciones,codigo,cantidad,precio_unitario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO detalle_cotizaciones (idcotizaciones, codigo, cantidad,  precio_unitario) VALUES (?, ?, ?,?)",
                       (idcotizaciones, codigo, cantidad, precio_unitario))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_detalle_cotizaciones():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.idcotizaciones, 
                cl.nombre AS nombre_cliente, 
                cl.ruc_dni, 
                cl.agencia_entrega, 
                cl.forma_entrega, 
                c.fecha 
            FROM 
                cotizaciones c
            JOIN 
                clientes cl ON c.idcliente = cl.idcliente
        """)
        rows = cursor.fetchall()
        conn.close()

        resultados = []
        for row in rows:
            print(f"Registro obtenido: {row}")  # Imprime cada fila obtenida
            resultados.append({
                'idcotizacion': row[0],
                'nombre_cliente': row[1],
                'ruc_dni': row[2],
                'agencia_entrega': row[3],
                'forma_entrega': row[4],
                'fecha': row[5]
            })

        return resultados

    @staticmethod
    def buscar_por_cliente(cliente):
        """
        Buscar cotizaciones por el nombre o ID del cliente en la base de datos SQL Server.
        """
        conn = get_connection()
        if conn is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return []

        cursor = conn.cursor()

        try:
            print(f"Buscando cotizaciones para el cliente: '{cliente}'")
            
            # Consulta SQL para buscar cotizaciones por nombre o ID del cliente
            query = """
            SELECT 
                c.idcotizaciones, 
                cl.nombre AS nombre_cliente, 
                cl.ruc_dni, 
                cl.agencia_entrega, 
                cl.forma_entrega, 
                c.fecha 
            FROM cotizaciones c
            JOIN clientes cl ON c.idcliente = cl.idcliente
            WHERE cl.nombre LIKE ?
            """
            
            # Ejecutar la consulta con los parámetros correspondientes
            cursor.execute(query, ('%' + cliente + '%',))

            cotizaciones = cursor.fetchall()
            print(f"Resultados obtenidos: {cotizaciones}")

            # Convertir los resultados en una lista de diccionarios
            return [{'idcotizacion': row[0], 'nombre_cliente': row[1], 'ruc_dni': row[2], 'agencia_entrega': row[3], 'forma_entrega': row[4], 'fecha': row[5]} for row in cotizaciones]
        
        except Exception as e:
            print(f"Error al buscar cotizaciones: {e}")
            return []
        
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()
