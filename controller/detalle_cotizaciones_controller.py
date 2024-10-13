from PyQt5 import uic
from datetime import datetime, date
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTableWidget
from model.detalle_cotizaciones import DetalleCotizaciones 
from views.detalle_cotizaciones_view import DetalleCotizacionesView

class DetalleCotizacionesController:
    def __init__(self):
        self.view = DetalleCotizacionesView()
        self.init_ui()
        self.load_historial()

        # Conectando botones a sus funciones
        #self.view.btn_editar.clicked.connect(self.editar_cotizacion)
        #self.view.btn_buscar.clicked.connect(self.buscar)
        self.view.btn_salir.clicked.connect(self.salir)

    def init_ui(self):
        self.view.tabla_cotizaciones.setColumnCount(6)  # Configura 6 columnas
        self.view.tabla_cotizaciones.setHorizontalHeaderLabels(["Nro ", "Cliente", "RUC o DNI", "Agencia Entrega", "Forma Entrega", "Fecha"])
        self.view.tabla_cotizaciones.setEditTriggers(QTableWidget.NoEditTriggers)
        self.view.tabla_cotizaciones.setSelectionBehavior(QTableWidget.SelectRows)

        self.view.tabla_cotizaciones.setColumnWidth(0, 50)  # Nro Cotización
        self.view.tabla_cotizaciones.setColumnWidth(1, 230)  # 
        self.view.tabla_cotizaciones.setColumnWidth(2, 120)  # RUC o DNI
        self.view.tabla_cotizaciones.setColumnWidth(3, 160)  # Agencia Entrega
        self.view.tabla_cotizaciones.setColumnWidth(4, 130)  # Forma Entrega
    
    def salir(self):
        self.view.close()
        

    def load_historial(self):
        cotizaciones = DetalleCotizaciones.obtener_detalle_cotizaciones()  # Obtener el historial de cotizaciones

        # Ordenar las cotizaciones por fecha
        def safe_parse_date(cotizacion):
            fecha = cotizacion['fecha']
            # Verifica si es un objeto de fecha, y devuelve como tal
            if isinstance(fecha, (datetime, date)):  # Usa `date` también aquí
                return fecha
            try:
                # Ajusta el formato de fecha según sea necesario
                return datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                # Devuelve una fecha muy lejana para que esas cotizaciones vayan al final
                return datetime.max

        cotizaciones.sort(key=safe_parse_date, reverse = True)

        self.view.tabla_cotizaciones.setRowCount(0)  # Reiniciar la tabla

        for cotizacion in cotizaciones:
            print(f"Insertando cotización en la tabla: {cotizacion}")  # Imprime la cotización que se va a insertar
            rowPosition = self.view.tabla_cotizaciones.rowCount()
            self.view.tabla_cotizaciones.insertRow(rowPosition)

            # Accede a los elementos del diccionario correctamente
            self.view.tabla_cotizaciones.setItem(rowPosition, 0, QTableWidgetItem(str(cotizacion['idcotizacion'])))
            self.view.tabla_cotizaciones.setItem(rowPosition, 1, QTableWidgetItem(cotizacion['nombre_cliente']))
            self.view.tabla_cotizaciones.setItem(rowPosition, 2, QTableWidgetItem(cotizacion['ruc_dni']))
            self.view.tabla_cotizaciones.setItem(rowPosition, 3, QTableWidgetItem(cotizacion['agencia_entrega']))
            self.view.tabla_cotizaciones.setItem(rowPosition, 4, QTableWidgetItem(cotizacion['forma_entrega']))
            self.view.tabla_cotizaciones.setItem(rowPosition, 5, QTableWidgetItem(str(cotizacion['fecha'])))

    