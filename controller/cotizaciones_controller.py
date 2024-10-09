from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QInputDialog, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from views.cotizaciones_view import CotizacionesView 
from views.detalle_cotizaciones_view import DetalleCotizacionesView 
from model.cotizaciones import Cotizaciones
from model.product import Productos  # Asegúrate de importar el modelo de productos
from model.clientes import Clientes
class CotizacionesController:
    def __init__(self):
        self.view = CotizacionesView()
        self.init_ui()
        self.productos = []
        
        self.load_clientes()  # Cargar clientes en el comboBox
        self.load_productos()  # Cargar productos en el comboBo

        
        self.view.guardarCotizacionButton.clicked.connect(self.save_cotizacion_as_pdf)
        self.view.addButton.clicked.connect(self.add_cotizacion)
        self.view.historialButton.clicked.connect(self.historial)
        self.view.newButton.clicked.connect(self.clear_table_and_fields)
        self.view.deleteProducto.clicked.connect(self.delete_producto)
        self.view.cotizacionTable.cellClicked.connect(self.on_table_cell_clicked)
        self.view.exitButton.clicked.connect(self.exit)

        # Conectar el evento de selección de producto para que actualice el precio
        self.view.productoComboBox.currentIndexChanged.connect(self.on_producto_changed)

    def load_clientes(self):
        # Aquí cargarías los clientes desde tu modelo
        clientes = Clientes.fetch_all()  # Asegúrate de implementar este método
        for cliente in clientes:
            self.view.clienteComboBox.addItem(cliente.nombre)

    def load_productos(self):
        # Aquí cargas los productos en el comboBox de tu ventana
        productos = Productos.fetch_all()  # Asegúrate de implementar este método
        self.productos = productos  # Almacena la lista de productos

        # Ordenar los productos por nombre
        self.productos.sort(key=lambda producto: producto.nombre)  # Ordenar en orden alfabético
        
        for prod in productos:
            self.view.productoComboBox.addItem(prod.nombre)  # Suponiendo que tienes un atributo 'nombre'      
        
        # Forzar la actualización del precio del primer producto
        if self.view.productoComboBox.count() > 0:  # Verifica que haya productos
            self.view.productoComboBox.setCurrentIndex(0)  # Selecciona el primer producto
            self.on_producto_changed()  # Actualiza el precio

    def historial(self):
        self.show_historial_controller()
    
    def show_historial_controller(self):
        self.historial_controller = DetalleCotizacionesView()
        self.historial_controller.show()

    def init_ui(self):
        self.view.cotizacionTable.setColumnCount(4)
        self.view.cotizacionTable.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio S/.", "Total"])
        self.view.cotizacionTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.view.cotizacionTable.setSelectionBehavior(QTableWidget.SelectRows)

        self.view.cotizacionTable.setColumnWidth(0, 260)

        self.view.fechaDateEdit.setCalendarPopup(True)  # Habilitar el popup del calendario
        self.view.fechaDateEdit.setDate(QDate.currentDate())
    
    def delete_producto(self):
        # Obtener la fila seleccionada
        selected_row = self.view.cotizacionTable.currentRow()
        if selected_row >= 0:  # Verifica que haya una fila seleccionada
            # Preguntar al usuario si está seguro de eliminar el producto
            confirm = QMessageBox.question(
                self.view, 
                "Confirmar Eliminación", 
                "¿Estás seguro de que deseas eliminar este producto?", 
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                # Eliminar la fila de la tabla
                self.view.cotizacionTable.removeRow(selected_row)
                self.update_total()  # Actualiza el total después de eliminar el producto
        else:
            QMessageBox.warning(self.view, "Error", "Por favor, selecciona un producto para eliminar.")
    
   
    def exit(self):
        self.view.close()

    '''def load_cotizaciones(self):
        cotizaciones = Cotizaciones.fetch_all()
        self.view.cotizacionTable.setRowCount(0) 
        
        for cotizacion in cotizaciones:
            rowPosition = self.view.cotizacionTable.rowCount()
            self.view.cotizacionTable.insertRow(rowPosition)
            self.view.cotizacionTable.setItem(rowPosition, 0, QTableWidgetItem(str(cotizacion.id)))
            self.view.cotizacionTable.setItem(rowPosition, 1, QTableWidgetItem(cotizacion.cliente))
            self.view.cotizacionTable.setItem(rowPosition, 2, QTableWidgetItem(cotizacion.fecha))
            self.view.cotizacionTable.setItem(rowPosition, 3, QTableWidgetItem(str(cotizacion.total)))'''

    
    def on_producto_changed(self):
        # Obtener el producto seleccionado
        index = self.view.productoComboBox.currentIndex()
        if index >= 0:  # Verifica que el índice sea válido
            producto_seleccionado = self.productos[index]  # Obtén el producto de la lista
            precio = producto_seleccionado.precio  # Asume que el objeto producto tiene el atributo 'precio'
            self.view.precioLineEdit.setText(str(precio))  # Muestra el precio en el LineEdit (o donde corresponda)
        else:
            self.view.precioLineEdit.clear()

    def add_cotizacion(self):
        try:
            cliente = self.view.clienteComboBox.currentText()
            producto = self.view.productoComboBox.currentText()
            cantidad = int(self.view.cantidadLineEdit.text())
            precio_unitario = float(self.view.precioLineEdit.text())  # Ahora obtiene el precio del LineEdit
            fecha_cotizacion = self.view.fechaDateEdit.date().toString("dd/MM/yyyy")

            total = cantidad * precio_unitario
            self.view.cotizacionTable.insertRow(self.view.cotizacionTable.rowCount())
            rowPosition = self.view.cotizacionTable.rowCount() - 1
            self.view.cotizacionTable.setItem(rowPosition, 0, QTableWidgetItem(producto))
            self.view.cotizacionTable.setItem(rowPosition, 1, QTableWidgetItem(str(cantidad)))
            self.view.cotizacionTable.setItem(rowPosition, 2, QTableWidgetItem(str(precio_unitario)))
            self.view.cotizacionTable.setItem(rowPosition, 3, QTableWidgetItem(str(total)))

            self.update_total()  # Método para actualizar el total general
            self.clear_fields()

        except ValueError:
            QMessageBox.warning(self.view, "Error de Datos", "Por favor, ingresa todos los datos correctamente.")


    def get_precio_producto(self, producto):
        # Aquí implementas la lógica para obtener el precio de un producto específico
        return Productos.fetch_precio(producto)  # Debes implementar este método
    

    def update_total(self):
        total_general = 0
        for row in range(self.view.cotizacionTable.rowCount()):
            total_general += float(self.view.cotizacionTable.item(row, 3).text())
        self.view.totalLineEdit.setText(str(total_general))

    def clear_fields(self):
        self.view.cantidadLineEdit.clear()  # Limpia el campo de cantidad
        self.view.productoComboBox.setCurrentIndex(-1)  # Resetea el ComboBox de productos
        self.view.precioLineEdit.clear()  # Limpia el campo de precio
        
        
    def clear_table_and_fields(self):
        # Limpiar todas las filas en la tabla de cotizaciones
        # Limpiar campos de entrada
        self.view.cantidadLineEdit.clear()
        self.view.productoComboBox.setCurrentIndex(-1)
        self.view.precioLineEdit.clear()
        self.view.cotizacionTable.setRowCount(0)

    def on_table_cell_clicked(self, row, column):
        # Obtener los datos de la fila seleccionada
        producto = self.view.cotizacionTable.item(row, 0).text()  # Suponiendo que el producto está en la primera columna
        cantidad = self.view.cotizacionTable.item(row, 1).text()  # Suponiendo que la cantidad está en la segunda columna
        precio = self.view.cotizacionTable.item(row, 2).text()  # Suponiendo que el precio está en la tercera columna

        # Encontrar el índice del producto en el ComboBox
        index = self.view.productoComboBox.findText(producto)

        if index != -1:
            # Actualizar el ComboBox con el producto seleccionado
            self.view.productoComboBox.setCurrentIndex(index)
        
        # Actualizar el LineEdit con el precio y la cantidad
        self.view.precioLineEdit.setText(precio)
        self.view.cantidadLineEdit.setText(cantidad)
    
    def save_cotizacion(self):
        try:
            cliente = self.view.clienteComboBox.currentText()
            idcliente = Clientes.get_id_by_nombre(cliente)  # Necesitas implementar este método para obtener el ID del cliente
            fecha_cotizacion = self.view.fechaDateEdit.date().toString("yyyy-MM-dd")  # Formato de fecha para la base de datos

            # Guardar cada producto en la base de datos
            for row in range(self.view.cotizacionTable.rowCount()):
                producto = self.view.cotizacionTable.item(row, 0).text()
                cantidad = int(self.view.cotizacionTable.item(row, 1).text())
                precio_unitario = float(self.view.cotizacionTable.item(row, 2).text())
                total = float(self.view.cotizacionTable.item(row, 3).text())

                # Asume que el código del producto se obtiene de alguna manera
                codigo = Productos.get_codigo_by_nombre(producto)  # Debes implementar este método

                # Llama al método para crear la cotización en la base de datos
                Cotizaciones.create(idcliente, fecha_cotizacion, codigo, cantidad, precio_unitario, total, estado="activo")

            QMessageBox.information(self.view, "Guardado", "Cotización guardada en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error al guardar la cotización: {e}")



    def save_cotizacion_as_pdf(self):
        self.save_cotizacion()  # Guardar la cotización en la base de datos

        # Abrir un diálogo para seleccionar la ubicación y el nombre del archivo
        options = QFileDialog.Options()
        pdf_file, _ = QFileDialog.getSaveFileName(self.view, "Guardar Cotización", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if pdf_file:  # Verifica que el usuario haya seleccionado un archivo
            # Crear un objeto Canvas
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter  # Dimensiones de la página

            # Escribir título
            c.drawString(200, height - 50, "Cotización")

            # Escribir encabezados de la tabla
            c.drawString(100, height - 100, "Producto")
            c.drawString(300, height - 100, "Cantidad")
            c.drawString(400, height - 100, "Precio S/. ")
            c.drawString(500, height - 100, "Total")

            # Escribir los datos de la tabla
            y_position = height - 120  # Posición inicial en Y para los datos

            for row in range(self.view.cotizacionTable.rowCount()):
                producto = self.view.cotizacionTable.item(row, 0).text()
                cantidad = self.view.cotizacionTable.item(row, 1).text()
                precio = self.view.cotizacionTable.item(row, 2).text()
                total = self.view.cotizacionTable.item(row, 3).text()

                c.drawString(100, y_position, producto)
                c.drawString(300, y_position, cantidad)
                c.drawString(400, y_position, precio)
                c.drawString(500, y_position, total)

                y_position -= 20  # Espacio entre filas

            # Guardar el PDF
            c.save()

            # Confirmar al usuario que se ha guardado el PDF
            QMessageBox.information(self.view, "Guardado", "Cotización guardada como PDF.")
                