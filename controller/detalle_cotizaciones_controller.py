from PyQt5 import uic
from datetime import datetime, date
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTableWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from model.detalle_cotizaciones import DetalleCotizaciones 
from views.detalle_cotizaciones_view import DetalleCotizacionesView

class DetalleCotizacionesController:
    def __init__(self):
        self.view = DetalleCotizacionesView()
        self.init_ui()
        self.load_historial()

        # Conectando botones a sus funciones
        self.view.btn_buscar.clicked.connect(self.buscar)
        self.view.btn_salir.clicked.connect(self.salir)

        # Almacenar las cotizaciones originales para uso posterior
        self.cotizaciones_originales = DetalleCotizaciones.obtener_detalle_cotizaciones()
        self.mostrar_cotizaciones(self.cotizaciones_originales)

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
        self.mostrar_cotizaciones(cotizaciones)

    def mostrar_cotizaciones(self, cotizaciones):
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

    def buscar(self):
        self.show_buscar_cotizacion()

    def show_buscar_cotizacion(self):
        dialog = QDialog()
        dialog.setWindowTitle("Buscar Cotización")

        # Configurar layout y widgets
        layout = QVBoxLayout()
        
        label = QLabel("Ingrese el nombre del cliente:")
        layout.addWidget(label)
        
        line_edit_cliente = QLineEdit()
        layout.addWidget(line_edit_cliente)

        btn_buscar = QPushButton("Buscar")
        layout.addWidget(btn_buscar)

        dialog.setLayout(layout)

        # Conectar el botón a la función de búsqueda
        btn_buscar.clicked.connect(lambda: self.buscar_cotizacion(line_edit_cliente.text().strip(), dialog, line_edit_cliente))

        dialog.exec_()  # Mostrar el diálogo

    def buscar_cotizacion(self, cliente, dialog,line_edit_cliente):
        if not cliente:
            QMessageBox.warning(dialog, "Error", "Por favor, ingrese el nombre del cliente.")
            line_edit_cliente.clear()
            return
        
        cotizaciones = DetalleCotizaciones.buscar_por_cliente(cliente)

        if not cotizaciones:
            QMessageBox.information(dialog, "Resultado", "No se encontraron cotizaciones.")
            # Volver a mostrar todas las cotizaciones si no se encontraron resultados
            self.mostrar_cotizaciones(self.cotizaciones_originales)
            dialog.accept()  # Cerrar el diálogo
            return

        # Mostrar los resultados encontrados
        self.mostrar_cotizaciones(cotizaciones)

        dialog.accept()  # Cerrar el diálogo después de mostrar los resultados
