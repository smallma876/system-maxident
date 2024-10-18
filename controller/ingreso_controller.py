from PyQt5.QtWidgets import QInputDialog,QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from views.product_management_view import ProductManagementView
from controller.registrar_producto_dialog import RegistrarProductoDialog
from controller.editar_producto_dialog import EditarProductoDialog
from model.product import Productos
import openpyxl
from PyQt5.QtWidgets import QFileDialog

class IngresoController:
    def __init__(self):
        self.view = ProductManagementView()
        self.init_ui()
        self.load_product()
        self.view.addButton.clicked.connect(self.mostrar_registrar_producto)
        self.view.salidaButton.clicked.connect(self.agregar_o_descontar)
        self.view.editButton.clicked.connect(self.update_product)
        self.view.BuscarButton.clicked.connect(self.search_product)
        self.view.newButton.clicked.connect(self.clear_fields)
        self.view.productTable.cellClicked.connect(self.on_table_cell_clicked)
        self.view.btnSalir.clicked.connect(self.salir)
        #self.view.eliminarButton.clicked.connect(self.delete_product)
        self.view.reporte.clicked.connect(self.generate_report)

        self.view.idproductoInput.setReadOnly(True)
        self.view.stockInput.setReadOnly(True)  # QLineEdit para el stock
        self.view.idcategoriaInput.setDisabled(True)  # QComboBox para la categoría
        self.view.nombreInput.setReadOnly(True)
        self.view.precioInput.setReadOnly(True)

    def init_ui(self):
        # Limpiar el QComboBox antes de llenarlo
        self.view.idcategoriaInput.clear()
        
        # Añadir elementos al QComboBox con sus respectivos textos y valores
        self.view.idcategoriaInput.addItem("VENTA", 1)  # "VENTA" con ID 1
        self.view.idcategoriaInput.addItem("INSUMO", 2)

    def salir(self):
        self.view.close()
        from controller.menu_controller import MenuWindow
        self.menu_controller = MenuWindow()
        self.menu_controller.view.show()

    def load_product(self):
        products = Productos.fetch_all()
        
        # Diccionario para mapear IDs de categorías a nombres
        categoria_dict = {
            1: "VENTA",
            2: "INSUMO"
        }

        self.view.productTable.setRowCount(0)
        for product in products:
            rowPosition = self.view.productTable.rowCount()
            self.view.productTable.insertRow(rowPosition)
            self.view.productTable.setItem(rowPosition, 0, QTableWidgetItem(str(product.codigo)))
            self.view.productTable.setItem(rowPosition, 1, QTableWidgetItem(product.nombre))
            
            # Usar el diccionario para obtener el nombre de la categoría
            categoria_nombre = categoria_dict.get(product.idcategoria, "Desconocido")  # Usa "Desconocido" si el ID no está en el diccionario
            self.view.productTable.setItem(rowPosition, 2, QTableWidgetItem(categoria_nombre))
            
            self.view.productTable.setItem(rowPosition, 3, QTableWidgetItem(str(product.precio)))
            self.view.productTable.setItem(rowPosition, 4, QTableWidgetItem(str(product.stock)))
        
            self.view.productTable.setColumnWidth(1, 230)
            self.view.productTable.setColumnWidth(2, 160)
            self.view.productTable.setColumnWidth(0, 70)
            self.view.productTable.setColumnWidth(3, 150)

            # Desactivar la edición de celdas
        self.view.productTable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Establecer selección por filas
        self.view.productTable.setSelectionBehavior(QTableWidget.SelectRows)

    def mostrar_registrar_producto(self):
        dialog = RegistrarProductoDialog(self.view)
        if dialog.exec_():
            # Refrescar el tablero de productos después del registro
            self.load_product()


    def agregar_o_descontar(self):
        codigo = self.view.idproductoInput.text()
        producto = Productos.search(codigo)
        
        if producto:
            cantidad, ok = QInputDialog.getInt(self.view, "CANTIDAD", "CUANTO DESEAS AGREGAR O DESCONTAR?", 0)

            if ok:
                if cantidad > 0:
                    nuevo_stock = producto.stock + cantidad  # Agregar stock
                else:
                    cantidad = abs(cantidad)  # Asegurarse de que sea un número positivo
                    nuevo_stock = producto.stock - cantidad  # Descontar stock

                    if nuevo_stock < 0:
                        QMessageBox.warning(self.view, "ERROR DE STOCK", "LA CANTIDAD DE SALIDA ES MAYOR DE LA CANTIDAD ACTUAL.")
                        return

                # Actualizar el stock en la base de datos
                Productos.update(codigo, producto.nombre, producto.idcategoria, producto.precio, nuevo_stock)
                QMessageBox.information(self.view, "SISTEMA", "STOCK ACTUALIZADO CON EXITO")
                self.load_updated_product(codigo)  # Cargar solo el producto actualizado

                # Actualizar el QLineEdit que muestra el stock
                self.view.stockInput.setText(str(nuevo_stock))  # Asumiendo que 'stockInput' es el QLineEdit correspondiente
        else:
            QMessageBox.warning(self.view, "Error", "SELECCIONA UN PRODUCTO")

    
    def update_product(self):
            # Obtener los datos de los campos
        row = self.view.productTable.currentRow()
        if row == -1:
            QMessageBox.warning(self.view, "ERROR", "Por favor selecciona un producto para editar.")
            return

        # Obtener datos actuales del cliente seleccionado
        codigo = self.view.productTable.item(row, 0).text()
        nombre_actual = self.view.productTable.item(row, 1).text()
        categoria_nombre = self.view.productTable.item(row, 2).text()
        precio_actual = self.view.productTable.item(row, 3).text()
        stock_actual = self.view.productTable.item(row, 4).text()

        idcategoria = 1 if categoria_nombre =="VENTA" else 2

        dialogo = EditarProductoDialog(nombre_actual,idcategoria,precio_actual,stock_actual)
        if dialogo.exec_() == QDialog.Accepted:
            # Obtener los valores del formulario
            nuevo_nombre = dialogo.nombre_input.text().upper()
            categoria = dialogo.categoria_input.currentText()
            nuevo_precio = dialogo.precio_input.text()
            nuevo_stock = dialogo.stock_input.text()

                # Mapear la nueva categoría al ID
            if categoria == "VENTA":
                idcategoria = 1
            elif categoria == "INSUMO":
                idcategoria = 2
            else:
                QMessageBox.warning(self.view, "Error", "Categoría no válida.")
                return
            
            # Confirmar cambios
            confirmar = QMessageBox.question(self.view, "Confirmar", "¿Seguro que deseas actualizar este producto?", QMessageBox.Yes | QMessageBox.No)
            if confirmar == QMessageBox.No:
                return
            
            Productos.update(codigo,nuevo_nombre,idcategoria,nuevo_precio,nuevo_stock)
            QMessageBox.information(self.view, "Éxito", "Producto actualizado correctamente.")

            # Refrescar tabla
            self.load_product()



    def load_updated_product(self, codigo):
        producto = Productos.search(codigo)
        
        # Limpia la tabla antes de cargar el nuevo producto
        self.view.productTable.setRowCount(0)
        
        if producto:
            rowPosition = self.view.productTable.rowCount()
            self.view.productTable.insertRow(rowPosition)
            self.view.productTable.setItem(rowPosition, 0, QTableWidgetItem(str(producto.codigo)))
            self.view.productTable.setItem(rowPosition, 1, QTableWidgetItem(producto.nombre))
            
            # Diccionario para mapear IDs de categorías a nombres
            categoria_dict = {
                1: "VENTA",
                2: "INSUMO"
            }
            
            categoria_nombre = categoria_dict.get(producto.idcategoria, "Desconocido")
            self.view.productTable.setItem(rowPosition, 2, QTableWidgetItem(categoria_nombre))
            self.view.productTable.setItem(rowPosition, 3, QTableWidgetItem(str(producto.precio)))
            self.view.productTable.setItem(rowPosition, 4, QTableWidgetItem(str(producto.stock)))
            
            
        else:
            QMessageBox.warning(self.view, "Error", "No se encontró el producto actualizado.")



    #def delete_product(self):
        #codigo = self.view.idproductoInput.text()
        #Productos.delete(codigo)  # Asegúrate de que este método esté implementado
        #QMessageBox.information(self.view, "Éxito", "Producto eliminado con éxito")
        #self.load_product() 

    def search_product(self):
        # Solicitar el nombre del producto
        nombre, ok = QInputDialog.getText(self.view, "BUSCAR PRODUCTO", "INGRESA EL NOMBRE DE TU PRODUCTO:")
        
        if ok and nombre:
            # Buscar productos por nombre
            products = Productos.search_by_name(nombre)  # Asumiendo que modificamos el método para devolver una lista
            
            self.view.productTable.setRowCount(0)  # Limpiar la tabla antes de agregar nuevos productos
            
            # Diccionario para mapear IDs de categorías a nombres
            categoria_dict = {
                1: "VENTA",
                2: "INSUMO"
            }

            if products:
                for product in products:
                    rowPosition = self.view.productTable.rowCount()
                    self.view.productTable.insertRow(rowPosition)
                    self.view.productTable.setItem(rowPosition, 0, QTableWidgetItem(str(product.codigo)))
                    self.view.productTable.setItem(rowPosition, 1, QTableWidgetItem(product.nombre))
                    categoria_nombre = categoria_dict.get(product.idcategoria, "Desconocido")
                    self.view.productTable.setItem(rowPosition, 2, QTableWidgetItem(categoria_nombre))
                    self.view.productTable.setItem(rowPosition, 3, QTableWidgetItem(str(product.precio)))
                    self.view.productTable.setItem(rowPosition, 4, QTableWidgetItem(str(product.stock)))
            else:
                QMessageBox.warning(self.view, "NO ENCONTRADO", "NO SE ENCONTRARON PRODUCTOS CON ESE NOMBRE.")


    def clear_fields(self):
        self.view.idproductoInput.clear()
        self.view.nombreInput.clear()
        self.view.precioInput.clear()
        self.view.stockInput.clear()

        self.load_product()

    def on_table_cell_clicked(self, row, column):
        codigo = self.view.productTable.item(row, 0).text()
        nombre = self.view.productTable.item(row, 1).text()
        categoria_nombre = self.view.productTable.item(row, 2).text()  # Obtén el nombre de la categoría
        
        # Mapear el nombre a su ID
        categoria_dict = {
            "VENTA": 1,
            "INSUMO": 2
        }
        idcategoria = categoria_dict.get(categoria_nombre)  # Obtén el ID correspondiente

        precio = self.view.productTable.item(row, 3).text()
        stock = self.view.productTable.item(row, 4).text()
        self.view.idproductoInput.setText(codigo)
        self.view.nombreInput.setText(nombre)
        
        # Usar findData para establecer el índice del QComboBox
        index = self.view.idcategoriaInput.findData(idcategoria)
        if index != -1:
            self.view.idcategoriaInput.setCurrentIndex(index)  # Establece el índice del QComboBox
        else:
            # Opcional: Manejo de caso donde no se encuentra la categoría
            QMessageBox.warning(self.view, "Error", "Categoría no encontrada en el combo box")
            
        self.view.precioInput.setText(precio)
        self.view.stockInput.setText(stock)

        
    def generate_report(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self.view, "Guardar Reporte", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
            if not file_path:
                return  

            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Reporte de Productos"
            headers = ["Codigo", "Nombre", "ID Categoría", "Precio", "Stock"]
            sheet.append(headers)
            products = Productos.fetch_all()
            for product in products:
                sheet.append([
                    product.codigo,
                    product.nombre,
                    product.idcategoria,
                    product.precio,
                    product.stock
                ])
            workbook.save(file_path)
            QMessageBox.information(self.view, "Éxito", "Reporte generado con éxito")

        except Exception as e:
            QMessageBox.warning(self.view, "Error", f"Ocurrió un error al generar el reporte: {str(e)}")
