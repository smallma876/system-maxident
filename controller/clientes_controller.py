from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem ,QTableWidget, QInputDialog
from views.clientes_view import ClientesView
from model.clientes import Clientes

class ClientesController:
    def __init__(self):
        self.view = ClientesView()
        self.cargar_clientes()
        self.view.boton_salir.clicked.connect(self.salir)
        self.view.boton_nuevo.clicked.connect(self.limpiar_celdas)
        self.view.boton_registrar.clicked.connect(self.registrar_cliente)
        #self.view.boton_editar.clicked.connect(self.editar_cliente)
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
        try:
            # Paso 1: Pedir el nombre del cliente
            while True:
                nombre, ok = QInputDialog.getText(self.view, "REGISTRAR CLIENTE", "NOMBRE DEL CLIENTE:")
                if not ok:
                    return  # Cancelar si el usuario no ingresa el nombre
                if nombre:  # Validar que el nombre no esté vacío
                    nombre = nombre.upper()
                    # Verificar si ya existe un CLIENTE con el mismo nombre
                    existe_clientes = Clientes.search_by_name(nombre)
                    if existe_clientes:
                        QMessageBox.warning(self.view, "ATECION", "YA EXISTE UN CLIENTE CON ESE NOMBRE.")
                        return  # No continuar con la creación si ya existe
                    break
            # Paso 2: Pedir el RUC o DNI, con validación
            while True:
                ruc_dni, ok = QInputDialog.getText(self.view, "REGISTRAR CLIENTE", "INGRESA EL NUMERO DE RUC O DNI:")
                if not ok:
                    return  # Cancelar si el usuario no ingresa el RUC o DNI
                if ruc_dni.isdigit() and len(ruc_dni) in (8, 11):
                    resultado = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTÁS SEGURO DEL NÚMERO?", 
                                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                    if resultado == QMessageBox.Yes:
                        break  # El número es correcto, salir del bucle
                    elif resultado == QMessageBox.Cancel:
                        return  # Cancelar si el usuario cancela la operación
                else:
                    QMessageBox.warning(self.view, "ERROR", "Número de RUC o DNI incorrecto. Debe tener 8 o 11 dígitos.")
            
            #paso 3: 
            while True:
                direccion, ok = QInputDialog.getText(self.view, "REGISTRAR CLIENTE", "INGRESA LA DIRECCION DEL CLIENTE:")
                if not ok:
                    return  
                if direccion:
                    direccion = direccion.lower()
                resultado = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTAS SEGURO DE LA DIRECCION ?", 
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if resultado == QMessageBox.Yes:
                    break
                elif resultado == QMessageBox.Cancel:
                    return
            
            while True:
                telefono, ok = QInputDialog.getInt(self.view, "REGISTRAR CLIENTE", "INGRESA EL NUMERO DE TELEFONO:", 0, 0,1000000000)
                if not ok:
                    return  
                resultado = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTAS SEGURO DEl NUMERO ?", 
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if resultado == QMessageBox.Yes:
                    break
                elif resultado == QMessageBox.Cancel:
                    return
                
            while True:
                agencia_entrega, ok = QInputDialog.getText(self.view, "REGISTRAR CLIENTE", "INGRESA LA AGENCIA PARA SU ENTREGA")
                if not ok:
                    return  
                if agencia_entrega:
                    agencia_entrega = agencia_entrega.lower()
                resultado = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTAS SEGURO DE LA AGENCIA ?", 
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if resultado == QMessageBox.Yes:
                    break
                elif resultado == QMessageBox.Cancel:
                    return
                
            while True:
                forma_entrega, ok = QInputDialog.getText(self.view, "REGISTRAR CLIENTE", "INGRESA SI ES A DOMICILIO O AGENCIA")
                if not ok:
                    return  
                if forma_entrega:
                    forma_entrega = forma_entrega.lower()
                resultado = QMessageBox.question(self.view, "CONFIRMAR", "¿ESTAS SEGURO PARA CONFIRMAR ?", 
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if resultado == QMessageBox.Yes:
                    break
                elif resultado == QMessageBox.Cancel:
                    return
            
            Clientes.create(nombre,telefono,direccion,agencia_entrega,ruc_dni,forma_entrega)
            QMessageBox.information(self.view, "SISTEMA", "¡CLIENTE REGISTRADO CON EXITO!")
            self.cargar_clientes()
            self.limpiar_celdas()

        except ValueError:
            QMessageBox.warning(self.view, "ERROR DE DATOS", "PORFAVOR INGRESA TODOS LOS DATOS CORRECTAMENTE")
    
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
        