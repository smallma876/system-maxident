from decimal import Decimal, ROUND_HALF_UP
from PyQt5.QtWidgets import QFileDialog, QCompleter, QInputDialog, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from views.cotizaciones_view import CotizacionesView 
from model.detalle_cotizaciones import DetalleCotizaciones
from model.cotizaciones import Cotizaciones
from model.product import Productos  
from model.clientes import Clientes
from controller.detalle_cotizaciones_controller import DetalleCotizacionesController

class CotizacionesController:
    def __init__(self):
        self.view = CotizacionesView()
        self.init_ui()
        self.productos = []
        self.load_clientes()  # Cargar clientes en el QLineEdit
        self.load_productos()  # Cargar productos en el QLineEdit
        self.view.guardarCotizacionButton.clicked.connect(self.save_cotizacion_as_pdf)
        self.view.addButton.clicked.connect(self.add_items_on_table)
        self.view.historialButton.clicked.connect(self.historial)
        self.view.newButton.clicked.connect(self.clear_table_and_fields)
        self.view.deleteProducto.clicked.connect(self.delete_producto)
        self.view.cotizacionTable.cellClicked.connect(self.on_table_cell_clicked)
        self.view.exitButton.clicked.connect(self.exit)

        self.view.productoLineEdit.textChanged.connect(self.on_producto_changed)
        # Configurar QCompleter para productos y clientes
        self.setup_completers()

    def setup_completers(self):
        # Para el QLineEdit de productos
        productos_nombres = [producto.nombre for producto in self.productos]
        completer_productos = QCompleter(productos_nombres, self.view.productoLineEdit)
        completer_productos.setCaseSensitivity(False)
        self.view.productoLineEdit.setCompleter(completer_productos)

        # Para el QLineEdit de clientes
        clientes_nombres = [cliente.nombre for cliente in Clientes.fetch_all()]
        completer_clientes = QCompleter(clientes_nombres, self.view.clienteLineEdit)
        completer_clientes.setCaseSensitivity(False)
        self.view.clienteLineEdit.setCompleter(completer_clientes)

    def load_clientes(self):
        clientes = Clientes.fetch_all()  
        for cliente in clientes:
            # Agregar cliente a una lista (no necesario en el QLineEdit)
            pass

    def load_productos(self):
        productos = Productos.fetch_all()  
        self.productos = productos  # Almacena la lista de productos

        # Ordenar los productos por nombre
        self.productos.sort(key=lambda producto: producto.nombre)  # Ordenar en orden alfabético

    def historial(self):
        self.show_historial_controller()
    
    def show_historial_controller(self):
        self.historial_controller = DetalleCotizacionesController()
        self.historial_controller.view.show()

    def init_ui(self):
        self.view.cotizacionTable.setColumnCount(4)
        self.view.cotizacionTable.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio S/.", "SubTotal"])
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
        from controller.menu_controller import MenuWindow
        self.menu_controller = MenuWindow()
        self.menu_controller.view.show()

    def on_producto_changed(self):
        # Obtener el producto seleccionado desde el LineEdit
        producto_text = self.view.productoLineEdit.text()
        producto_seleccionado = next((producto for producto in self.productos if producto.nombre == producto_text), None)
        
        if producto_seleccionado:
            precio = producto_seleccionado.precio  # Asume que el objeto producto tiene el atributo 'precio'
            self.view.precioLineEdit.setText(str(precio))  # Muestra el precio en el LineEdit
        else:
            self.view.precioLineEdit.clear()

    def add_items_on_table(self):
        try:
            producto = self.view.productoLineEdit.text()  # Cambiado a QLineEdit
            cantidad = int(self.view.cantidadLineEdit.text())
            precio_unitario = Decimal(self.view.precioLineEdit.text())  # Ahora obtiene el precio del LineEdit
            subtotal = (precio_unitario * Decimal(cantidad)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 

            self.view.cotizacionTable.insertRow(self.view.cotizacionTable.rowCount())
            rowPosition = self.view.cotizacionTable.rowCount() - 1
            self.view.cotizacionTable.setItem(rowPosition, 0, QTableWidgetItem(producto))
            self.view.cotizacionTable.setItem(rowPosition, 1, QTableWidgetItem(str(cantidad)))
            self.view.cotizacionTable.setItem(rowPosition, 2, QTableWidgetItem(str(precio_unitario)))
            self.view.cotizacionTable.setItem(rowPosition, 3, QTableWidgetItem(str(subtotal)))

            self.update_total()  # Método para actualizar el total general
            self.clear_fields()

        except ValueError:
            QMessageBox.warning(self.view, "ATENCION", "POR FAVOR, COMPLETA TODOS LOS CAMPOS.")

    def update_total(self):
        total_general = Decimal(0)
        for row in range(self.view.cotizacionTable.rowCount()):
            total_general += Decimal(self.view.cotizacionTable.item(row, 3).text())
        
        total_general = total_general.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Redondear a 2 decimales
        self.view.totalLineEdit.setText(str(total_general))

    def clear_fields(self):
        self.view.cantidadLineEdit.clear()  # Limpia el campo de cantidad
        self.view.productoLineEdit.clear()  # Limpia el campo de producto
        self.view.precioLineEdit.clear()  # Limpia el campo de precio
        self.view.totalLineEdit.clear()

    def clear_table_and_fields(self):
        self.view.cotizacionTable.setRowCount(0)
        self.clear_fields()

    def on_table_cell_clicked(self, row, column):
        # Obtener los datos de la fila seleccionada
        producto = self.view.cotizacionTable.item(row, 0).text()
        cantidad = self.view.cotizacionTable.item(row, 1).text()
        precio = self.view.cotizacionTable.item(row, 2).text()

        # Establecer el texto del LineEdit de producto
        self.view.productoLineEdit.setText(producto)
        self.view.cantidadLineEdit.setText(cantidad)
        self.view.precioLineEdit.setText(precio)

    def obtener_producto_codigo(self, nombre):
        codigo = Productos.obtener_productos(nombre)  # Aquí pasamos el nombre como argumento
        if codigo:
            return codigo
        return None

    def save_cotizacion(self):
        cliente = self.view.clienteLineEdit.text()
        idcliente = Clientes.get_id_by_nombre(cliente)  # Obtén el ID del cliente
        fecha = self.view.fechaDateEdit.date().toString("yyyy-MM-dd")  # Formato de fecha para la base de datos
        idcotizaciones = Cotizaciones.create(idcliente, fecha)
        total = 0.0  
        # Guardar cada producto en la base de datos
        for row in range(self.view.cotizacionTable.rowCount()):
            nombre = self.view.cotizacionTable.item(row, 0).text()
            codigo = self.obtener_producto_codigo(nombre)
            if codigo is None:
                raise Exception(f"Producto '{nombre}' no encontrado.")

            cantidad = int(self.view.cotizacionTable.item(row, 1).text())
            precio_unitario = Decimal(self.view.cotizacionTable.item(row, 2).text())  # Cambié a la columna 3 para obtener el subtotal
            subtotal = float(self.view.cotizacionTable.item(row, 3).text()) 

            DetalleCotizaciones.agregar_detalle_cotizacion(idcotizaciones, codigo, cantidad, precio_unitario)
            total += subtotal  # Sumar al total
        
        Cotizaciones.update_total(idcotizaciones, total)
            
    
    def save_cotizacion_as_pdf(self):
        # Verificar si hay productos en la tabla
        if self.view.cotizacionTable.rowCount() == 0:
            QMessageBox.warning(self.view, "Advertencia", "No hay ningún producto seleccionado.")
            return  # Salir del método si no hay productos

        # Preguntar al usuario si está seguro de guardar la cotización
        confirm = QMessageBox.question(
            self.view,
            "Confirmar Guardado",
            "¿Estás seguro de que deseas guardar esta cotización?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.save_cotizacion()

        elif confirm == QMessageBox.No:
            return  # Salir si el usuario cancela

        # Elegir la ubicación para guardar el PDF
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Guardar Cotización como PDF", "", "PDF Files (*.pdf)", options=options)

        if not file_path:
            return  # El usuario canceló el diálogo

        # Obtener el nombre del cliente y su RUC/DNI
        cliente_nombre = self.view.clienteLineEdit.text()
        ruc_dni = Clientes.get_ruc_dni(cliente_nombre)  # Asegúrate de tener este método

        # Crear el lienzo (canvas) para el PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter  # Tamaño de página Carta

        # Logo
        logo_path = "file:///D:/Proyectos/system-maxident/ui/Imagenes/Imagen%20de%20WhatsApp%202024-08-13%20a%20las%2020.52.17_e647f5ba.jpg"
        if logo_path:
            c.drawImage(logo_path, 430, height - 185, width=120, height=100)

        # Título
        c.setFillColorRGB(0, 0.2, 0.4)
        c.setFont("Helvetica-Bold", 40)
        c.drawString(305, height - 65, "COTIZACIÓN")

        # Fecha actual de la cotización
        c.setFillColorRGB(0, 0, 0)
        fecha_actual = QDate.currentDate().toString("dd/MM/yyyy")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, f"Fecha: {fecha_actual}")  # Mueve la fecha a la izquierda

        # Título
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, height - 140, "COTIZACIÓN")

        # Agregar el nombre del cliente y su RUC/DNI
        c.setFillColorRGB(0, 0.2, 0.4)
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 165, f"Cliente: {cliente_nombre}")  # Nombre del cliente
        c.drawString(50, height - 185, f"RUC/DNI: {ruc_dni}")  # RUC/DNI del cliente

        # Encabezado de la tabla
        c.setFillColorRGB(0, 0.2, 0.4)  # Color azul oscuro
        c.setStrokeColorRGB(0, 0.2, 0.4)
        c.rect(50, height - 220, 500, 20, fill=1)

        # Texto en blanco para el encabezado
        c.setFillColorRGB(1, 1, 1)  # Texto blanco
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, height - 215, "Producto")  # Columna Producto
        c.drawString(360, height - 215, "Cantidad")  # Columna Cantidad
        c.drawString(430, height - 215, "Precio S/")  # Columna Precio S/
        c.drawString(500, height - 215, "Subtotal")  # Columna Subtotal

        # Datos de la tabla
        y_position = height - 240  # Posición inicial de las filas
        total_general = 0  # Variable para almacenar el total general

        for row in range(self.view.cotizacionTable.rowCount()):
            producto = self.view.cotizacionTable.item(row, 0).text()
            cantidad = self.view.cotizacionTable.item(row, 1).text()
            precio = self.view.cotizacionTable.item(row, 2).text()
            subtotal = self.view.cotizacionTable.item(row, 3).text()

            # Dibujar cada fila en el PDF
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0, 0, 0)  # Color del texto
            c.drawString(50, y_position, producto)  # Columna Producto
            c.drawString(375, y_position, cantidad)  # Columna Cantidad
            c.drawString(440, y_position, precio)  # Columna Precio S/
            c.drawString(510, y_position, subtotal)  # Columna Subtotal

            # Acumular el subtotal al total general
            total_general += float(subtotal)

            y_position -= 20  # Avanzar la posición vertical para la siguiente fila

            # Salto de página si se llena
            if y_position < 50:
                c.showPage()  # Iniciar una nueva página si se llega al final
                y_position = height - 50  # Reiniciar la posición en la nueva página

        # Total de la cotización
        c.setFont("Helvetica-Bold", 12)
        c.drawString(420, y_position - 20, f"Monto Total: S/ {total_general:.2f}")  # Mostrar el total con dos decimales

        # Guardar el PDF
        c.save()

        # Limpiar la tabla y los campos
        self.clear_table_and_fields()

        # Mostrar mensaje de éxito
        QMessageBox.information(self.view, "Éxito", "La cotización ha sido guardada como PDF.")

                        