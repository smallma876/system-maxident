from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem ,QTableWidget, QInputDialog,QDialog
from controller.editar_cliente import EditarClienteDialog
from views.clientes_view import ClientesView
from model.clientes import Clientes
from controller.crear_cliente import CrearClienteDialog

class ClientesController:
    def __init__(self):
        self.view = ClientesView()
        self.cargar_clientes()
        
        self.view.boton_salir.clicked.connect(self.salir)
        self.view.boton_nuevo.clicked.connect(self.limpiar_celdas)
        self.view.boton_registrar.clicked.connect(self.registrar_cliente)
        self.view.boton_editar.clicked.connect(self.editar_cliente)
        self.view.boton_buscar.clicked.connect(self.buscar_cliente)
        self.view.clientetable.cellClicked.connect(self.table_cell_clicked)

        self.view.idcliente.setReadOnly(True)
        self.view.clientenombre.setReadOnly(True)  
        self.view.clienteruc.setDisabled(True)  
        self.view.clientetelefono.setReadOnly(True)
        self.view.clienteagencia.setReadOnly(True)
        self.view.clientedireccion.setReadOnly(True)
        self.view.clienteformaentrega.setReadOnly(True)

    def salir(self):
        self.view.close()
        from controller.menu_controller import MenuWindow
        self.menu_controller = MenuWindow()
        self.menu_controller.view.show()

    def cargar_clientes(self):
        clientes = Clientes.fetch_all()

        self.view.clientetable.setRowCount(0)
        for cliente in clientes:
            rowPosition = self.view.clientetable.rowCount()
            self.view.clientetable.insertRow(rowPosition)
            self.view.clientetable.setItem(rowPosition, 0, QTableWidgetItem(str(cliente.idcliente)))
            self.view.clientetable.setItem(rowPosition, 1, QTableWidgetItem(cliente.nombre))
            self.view.clientetable.setItem(rowPosition, 2, QTableWidgetItem(str(cliente.ruc_dni)))
            self.view.clientetable.setItem(rowPosition, 3, QTableWidgetItem(str(cliente.direccion)))
            self.view.clientetable.setItem(rowPosition, 4, QTableWidgetItem(str(cliente.telefono)))
            self.view.clientetable.setItem(rowPosition, 5, QTableWidgetItem(str(cliente.agencia_entrega)))
            self.view.clientetable.setItem(rowPosition, 6, QTableWidgetItem(str(cliente.forma_entrega)))

            self.view.clientetable.setColumnWidth(0, 50)
            self.view.clientetable.setColumnWidth(1, 200)
            self.view.clientetable.setColumnWidth(2, 110)
            self.view.clientetable.setColumnWidth(3, 190)
            self.view.clientetable.setColumnWidth(5, 120)
            self.view.clientetable.setColumnWidth(6, 110)

           # Desactivar la edición de celdas
        self.view.clientetable.setEditTriggers(QTableWidget.NoEditTriggers)
        # Establecer selección por filas
        self.view.clientetable.setSelectionBehavior(QTableWidget.SelectRows)

    
    def registrar_cliente(self):
        dialogo = CrearClienteDialog(self.view)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_clientes()


    
    def editar_cliente(self):
        # Verificar que hay un cliente seleccionado
        row = self.view.clientetable.currentRow()
        if row == -1:
            QMessageBox.warning(self.view, "ERROR", "Por favor selecciona un cliente para editar.")
            return

        # Obtener datos actuales del cliente seleccionado
        idcliente = self.view.clientetable.item(row, 0).text()
        nombre_actual = self.view.clientetable.item(row, 1).text()
        ruc_dni_actual = self.view.clientetable.item(row, 2).text()
        direccion_actual = self.view.clientetable.item(row, 3).text()
        telefono_actual = self.view.clientetable.item(row, 4).text()
        agencia_entrega_actual = self.view.clientetable.item(row, 5).text()
        forma_entrega_actual = self.view.clientetable.item(row, 6).text()

        # Abrir el diálogo personalizado
        dialogo = EditarClienteDialog(nombre_actual, ruc_dni_actual, direccion_actual, telefono_actual, agencia_entrega_actual, forma_entrega_actual, self.view)
        if dialogo.exec_() == QDialog.Accepted:
            # Obtener los valores del formulario
            nuevo_nombre = dialogo.nombre_input.text().upper()
            nuevo_ruc_dni = dialogo.ruc_dni_input.text()
            nueva_direccion = dialogo.direccion_input.text()
            nuevo_telefono = dialogo.telefono_input.text()
            nueva_agencia_entrega = dialogo.agencia_entrega_input.text()
            nueva_forma_entrega = dialogo.forma_entrega_input.text()

            # Confirmar cambios
            confirmar = QMessageBox.question(self.view, "Confirmar", "¿Seguro que deseas actualizar este cliente?", QMessageBox.Yes | QMessageBox.No)
            if confirmar == QMessageBox.No:
                return

            # Actualizar en la base de datos
            Clientes.update(idcliente, nuevo_nombre, nuevo_telefono, nueva_direccion, nueva_agencia_entrega, nuevo_ruc_dni, nueva_forma_entrega)
            QMessageBox.information(self.view, "Éxito", "Cliente actualizado correctamente.")

            # Refrescar tabla
            self.cargar_clientes()



    def buscar_cliente(self):
        nombre, ok = QInputDialog.getText(self.view, "BUSCAR PRODUCTO", "INGRESA EL NOMBRE DEL CLIENTE:")
        if ok and nombre:
            clientes = Clientes.search_by_name(nombre)
            self.view.clientetable.setRowCount(0)

            if clientes:
                for cliente in clientes:
                    rowPosition = self.view.clientetable.rowCount()
                    self.view.clientetable.insertRow(rowPosition)
                    self.view.clientetable.setItem(rowPosition, 0, QTableWidgetItem(str(cliente.idcliente)))
                    self.view.clientetable.setItem(rowPosition, 1, QTableWidgetItem(cliente.nombre))
                    self.view.clientetable.setItem(rowPosition, 2, QTableWidgetItem(str(cliente.ruc_dni)))
                    self.view.clientetable.setItem(rowPosition, 3, QTableWidgetItem(str(cliente.direccion)))
                    self.view.clientetable.setItem(rowPosition, 4, QTableWidgetItem(str(cliente.telefono)))
                    self.view.clientetable.setItem(rowPosition, 5, QTableWidgetItem(str(cliente.agencia_entrega)))
                    self.view.clientetable.setItem(rowPosition, 6, QTableWidgetItem(str(cliente.forma_entrega)))
            else:
                QMessageBox.warning(self.view, "NO ENCONTRADO", "NO SE ENCONTRARON CLIENTES CON ESE NOMBRE.")


    def limpiar_celdas(self):
        self.view.idcliente.clear() 
        self.view.clientenombre.clear()
        self.view.clienteruc.clear() 
        self.view.clientetelefono.clear() 
        self.view.clienteagencia.clear() 
        self.view.clientedireccion.clear() 
        self.view.clienteformaentrega.clear() 
        self.cargar_clientes()

        
    def table_cell_clicked(self,row):
        idcliente = self.view.clientetable.item(row, 0).text()
        nombre = self.view.clientetable.item(row, 1).text()
        ruc_dni = self.view.clientetable.item(row, 2).text()
        direccion = self.view.clientetable.item(row, 3).text()
        telefono = self.view.clientetable.item(row, 4).text()
        agencia_entrega = self.view.clientetable.item(row, 5).text()
        forma_entrega = self.view.clientetable.item(row, 6).text()

        self.view.idcliente.setText(idcliente)
        self.view.clientenombre.setText(nombre)
        self.view.clienteruc.setText(ruc_dni)
        self.view.clientedireccion.setText(direccion)
        self.view.clientetelefono.setText(telefono)
        self.view.clienteagencia.setText(agencia_entrega)
        self.view.clienteformaentrega.setText(forma_entrega)
        