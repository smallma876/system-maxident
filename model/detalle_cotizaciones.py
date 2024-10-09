from model.database import get_connection 

class DetalleCotizaciones:
    def __init__(self, idcotizaciones, codigo, cantidad, precio_unitario):
        self.idcotizacion = idcotizaciones
        self.nombre = codigo
        self.ruc_dni = cantidad
        self.agencia_entrega = precio_unitario
        

    
    @staticmethod
    def create(idcotizaciones, codigo, cantidad, precio_unitario):
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO detalle_cotizaciones (ID, codigo, cantidad, precio_unitario, total) VALUES (?, ?, ?, ?)", 
                (idcotizaciones, codigo, cantidad, precio_unitario,)
            )
            connection.commit()