from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from views.product_management_view import ProductManagementView
from model.product import Productos
import openpyxl
from PyQt5.QtWidgets import QFileDialog

class IngresoController:
    def __init__(self):
        self.view = ProductManagementView()
        self.init_ui()
        self.load_product()
        self.view.addButton.clicked.connect(self.add_product)
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
        self.view.idcategoriaInput.addItem("PRODUCTO_VENTA", 1)  # "PRODUCTO_VENTA" con ID 1
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
            1: "PRODUCTO_VENTA",
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


    def add_product(self):
        try:
            # Paso 1: Pedir el nombre del producto
            while True:
                
                nombre, ok = QInputDialog.getText(self.view, "REGISTRAR PRODUCTO", "NOMBRE DEL PRODUCTO:")
                if not ok:
                    return  # Cancelar si el usuario no ingresa el nombre
                if nombre:  # Validar que el nombre no esté vacío
                    nombre = nombre.upper()
                    # Verificar si ya existe un producto con el mismo nombre
                    existing_products = Productos.search_by_name(nombre)
                    if existing_products:
                        QMessageBox.warning(self.view, "PRODUCTO DUPLICADO", "YA EXISTE UN PRODUCTO CON ESE NOMBRE.")
                        return  # No continuar con la creación si ya existe
                    break

            # Paso 2: Pedir la categoría (PRODUCTO_VENTA o INSUMO)
            categorias = ["PRODUCTO_VENTA", "INSUMO"]
            while True:
                categoria, ok = QInputDialog.getItem(self.view, "REGISTRAR PRODUCTO", "SELECCIONA LA CATEGORIA:", categorias, 0, False)
                if not ok:
                    return  # Cancelar si no se selecciona una categoría
                if categoria:
                    break

                # Paso 3: Pedir el stock
            while True:
                # Solicitar el stock del producto
                stock, ok = QInputDialog.getInt(self.view, "REGISTRAR PRODUCTO", "STOCK DEL PRODUCTO:", 0, 0, 1000000)
                
                # Cancelar si no se ingresa el stock
                if not ok:
                    return  

                # Opción de retroceder
                result = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTÁS SEGURO DE LA CANTIDAD?", 
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

                if result == QMessageBox.Yes:
                    # Si el usuario confirma, salir del bucle
                    break  
                elif result == QMessageBox.Cancel:
                    return  # Salir si el usuario cancela
                # Si elige No, el bucle se repetirá y se pedirá el stock nuevamente.


            # Paso 4: Si la categoría es "PRODUCTO_VENTA", pedir el precio
            if categoria == "PRODUCTO_VENTA":
                while True:
                    precio, ok = QInputDialog.getDouble(self.view, "REGISTRAR PRODUCTO", "PRECIO DEL PRODUCTO:", 0, 0, 1000000, 2)
                    if not ok:
                        return  # Cancelar si no se ingresa el precio
                    result = QMessageBox.question(self.view, "CONFIRMARr", "¿ESTAS SEGURO DE ESTE PRECIO?",
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                    if result == QMessageBox.Yes:
                        break  # Avanzar si está seguro
                    elif result == QMessageBox.Cancel:
                        return  # Salir si el usuario cancela
            else:
                precio = 0.0  # Para "INSUMO", el precio será 0

            # Mapear la categoría seleccionada al ID correspondiente
            idcategoria = 1 if categoria == "PRODUCTO_VENTA" else 2

            # Si no existe un producto con el mismo nombre, se crea el nuevo producto
            Productos.create(nombre, idcategoria, precio, stock)
            QMessageBox.information(self.view, "SISTEMA", "¡PRODUCTO AGREGADO CON EXITO!")
            self.load_product()
            self.clear_fields()
        except ValueError:
            QMessageBox.warning(self.view, "ERROR DE DATOS", "PORFAVOR INGRESA TODOS LOS DATOS CORRECTAMENTE")



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
        try:
            # Obtener el código del producto seleccionado
            codigo = self.view.idproductoInput.text()
            producto = Productos.search(codigo)  # Busca el producto en la base de datos
            
            if not producto:
                QMessageBox.warning(self.view, "Error", "SELECCIONA UN PRODUCTO.")
                return
            
            # Pedir nuevo nombre
            nuevo_nombre, ok = QInputDialog.getText(self.view, "EDITAR PRODUCTO", "NUEVO NOMBRE DEL PRODUCTO:", text=producto.nombre)
            if not ok or not nuevo_nombre:
                return  # Cancelar si no se ingresa un nuevo nombre
            if nuevo_nombre != producto.nombre:  # Si hay un cambio
                nuevo_nombre = nuevo_nombre.upper()
                confirm = QMessageBox.question(self.view, "Confirmación", f"¿Está seguro que desea cambiar el nombre de '{producto.nombre}' a '{nuevo_nombre}'?", QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.No:
                    return  # Cancelar si el usuario no está de acuerdo

            # Pedir nueva categoría
            categorias = ["PRODUCTO_VENTA", "INSUMO"]
            nueva_categoria, ok = QInputDialog.getItem(self.view, "EDITAR PRODUCTO", "SELECCIONA LA NUEVA CATEGORÍA:", categorias, 0, False)
            if not ok:
                return  # Cancelar si no se selecciona una categoría
            
            if nueva_categoria != ("PRODUCTO_VENTA" if producto.idcategoria == 1 else "INSUMO"):  # Si hay un cambio
                confirm = QMessageBox.question(self.view, "Confirmación", f"¿Está seguro que desea cambiar la categoría de '{('PRODUCTO_VENTA' if producto.idcategoria == 1 else 'INSUMO')}' a '{nueva_categoria}'?", QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.No:
                    return  # Cancelar si el usuario no está de acuerdo

            # Pedir nuevo stock
            nuevo_stock, ok = QInputDialog.getInt(self.view, "EDITAR PRODUCTO", "NUEVO STOCK DEL PRODUCTO:", value=producto.stock, min=0, max=1000000)
            if not ok:
                return  # Cancelar si no se ingresa un nuevo stock
            if nuevo_stock != producto.stock:  # Si hay un cambio
                confirm = QMessageBox.question(self.view, "Confirmación", f"¿Está seguro que desea cambiar el stock de {producto.stock} a {nuevo_stock}?", QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.No:
                    return  # Cancelar si el usuario no está de acuerdo

            # Si la categoría es "INSUMO", no se debe pedir precio y se establece en 0
            if nueva_categoria == "INSUMO":
                nuevo_precio = 0.0
            else:
                nuevo_precio, ok = QInputDialog.getDouble(self.view, "EDITAR PRODUCTO", "NUEVO PRECIO DEL PRODUCTO:", value=producto.precio, min=0, max=1000000, decimals=2)
                if not ok:
                    return  # Cancelar si no se ingresa un nuevo precio
                if nuevo_precio != producto.precio:  # Si hay un cambio
                    confirm = QMessageBox.question(self.view, "Confirmación", f"¿Está seguro que desea cambiar el precio de {producto.precio:.2f} a {nuevo_precio:.2f}?", QMessageBox.Yes | QMessageBox.No)
                    if confirm == QMessageBox.No:
                        return  # Cancelar si el usuario no está de acuerdo

            # Mapear la nueva categoría a su ID correspondiente
            idcategoria = 1 if nueva_categoria == "PRODUCTO_VENTA" else 2
            
            # Actualizar el producto en la base de datos
            Productos.update(codigo, nuevo_nombre, idcategoria, nuevo_precio, nuevo_stock)
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self.view, "Sistema", "PRODUCTO ACTUALIZADO CON ÉXITO")
            
            # Recargar los productos en la tabla
            self.load_product()

        except ValueError:
            QMessageBox.warning(self.view, "Error de Datos", "POR FAVOR INGRESA TODOS LOS DATOS CORRECTAMENTE")

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
                1: "PRODUCTO_VENTA",
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
                1: "PRODUCTO_VENTA",
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
            "PRODUCTO_VENTA": 1,
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
