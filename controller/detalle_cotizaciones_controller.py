from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from model.detalle_cotizaciones import HistorialCotizaciones  # Cambié a HistorialCotizaciones

class DetalleCotizacionesView:
    def __init__(self):
        self.view = DetalleCotizacionesView
        # Conectando botones a sus funciones
        self.view.btn_editar.clicked.connect(self.editar_cotizacion)
        self.view.btn_buscar.clicked.connect(self.buscar_cotizacion)
        self.view.btn_salir.clicked.connect(self.salir)

        # Inicializamos la tabla de cotizaciones (QTableWidget)
        self.view.tabla_cotizaciones.setColumnCount(6)  # Cambia a 6 ya que solo hay 6 columnas en tu consulta
        self.view.tabla_cotizaciones.setHorizontalHeaderLabels([
            "Nro Cotización", "Cliente", "RUC o DNI", "Agencia Entrega", 
            "Forma Entrega", "Fecha"
        ])

        # Cargar el historial al inicio
        self.load_historial()

    def salir(self):
        self.view.close()

    def load_historial(self):
        cotizaciones = HistorialCotizaciones.fetch_historial()  # Obtén el historial
        self.view.tabla_cotizaciones.setRowCount(0)  # Asegúrate de usar self.view aquí

        for cotizacion in cotizaciones:
            rowPosition = self.view.tabla_cotizaciones.rowCount()  # Asegúrate de usar self.view aquí
            self.view.tabla_cotizaciones.insertRow(rowPosition)
            self.view.tabla_cotizaciones.setItem(rowPosition, 0, QTableWidgetItem(str(cotizacion.idcotizacion)))  # Cambia a idcotizacion
            self.view.tabla_cotizaciones.setItem(rowPosition, 1, QTableWidgetItem(cotizacion.nombre))
            self.view.tabla_cotizaciones.setItem(rowPosition, 2, QTableWidgetItem(cotizacion.ruc_dni))
            self.view.tabla_cotizaciones.setItem(rowPosition, 3, QTableWidgetItem(cotizacion.agencia_entrega))  # Agrega este campo
            self.view.tabla_cotizaciones.setItem(rowPosition, 4, QTableWidgetItem(cotizacion.forma_entrega))  # Agrega este campo
            self.view.tabla_cotizaciones.setItem(rowPosition, 5, QTableWidgetItem(cotizacion.fecha))  # Cambia a 5 para la fecha