from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from model.product import Productos
class EditarProductoDialog(QDialog):
    def __init__(self, producto, parent=None):
        super().__init__(parent)
        self.producto = producto

        # Layout principal
        layout = QVBoxLayout(self)

        # Crear un formulario con todos los campos
        form_layout = QFormLayout()

        # Campos de edición
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setText(producto.nombre)  # Cargar el nombre del producto actual
        form_layout.addRow("Nombre del Producto:", self.nombre_input)

        # Cambiar QLineEdit por QComboBox para la categoría
        self.categoria_input = QComboBox(self)
        self.categoria_input.addItems(["VENTA", "INSUMO"])  # Añadir opciones
        # Seleccionar la categoría actual
        if producto.idcategoria == 1:
            self.categoria_input.setCurrentIndex(0)
        else:
            self.categoria_input.setCurrentIndex(1)
        form_layout.addRow("Categoría:", self.categoria_input)

        self.stock_input = QLineEdit(self)
        self.stock_input.setText(str(producto.stock))  # Cargar el stock actual
        form_layout.addRow("Stock:", self.stock_input)

        self.precio_input = QLineEdit(self)
        self.precio_input.setText(str(producto.precio))  # Cargar el precio actual
        form_layout.addRow("Precio por mayor:", self.precio_input)

        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()

        # Botón Aceptar (Editar)
        self.ok_button = QPushButton("Editar Producto", self)
        self.ok_button.setFixedSize(170, 40)  # Tamaño del botón
        self.ok_button.clicked.connect(self.editar_producto)
        button_layout.addWidget(self.ok_button)

        # Botón Cancelar
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.setFixedSize(170, 40)  # Tamaño del botón
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # Agregar el layout de botones al layout principal
        layout.addLayout(button_layout)

        self.resize(900, 250)

        # Aplicar los mismos estilos que en "Registrar Producto"
        self.setStyleSheet("""
            QDialog {
                background-color: white; /* Fondo blanco */
            }
            QLabel {
                color: black;
                font-size: 20px;
                font-weight: bold;
                background-color: white;
            }
            QLineEdit {
                background-color: #4c4c4c;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 1px solid #5c5c5c;
            }
            QComboBox {
                background-color: #4c4c4c;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 1px solid #5c5c5c;
            }
            QPushButton {
                background-color: #004466;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #046697;
            }
        """)

    def editar_producto(self):
        try:
            # Obtener los datos de los campos
            
            
            nombre = self.nombre_input.text()
            categoria = self.categoria_input.currentText()
            stock = int(self.stock_input.text())
            precio = float(self.precio_input.text())

            # Validaciones de entrada
            if not nombre or stock < 0 or precio < 0:
                QMessageBox.warning(self, "Error", "Por favor, completa todos los campos correctamente.")
                return

            # Convertir la categoría a ID
            idcategoria = 1 if categoria == "VENTA" else 2

            # Lógica para actualizar el producto en la base de datos
            success = Productos.update(codigo, nombre, idcategoria, precio, stock)

            if success:
                QMessageBox.information(self, "Éxito", "Producto actualizado con éxito.")
                self.accept()  # Cerrar el diálogo si la actualización fue exitosa
            else:
                QMessageBox.warning(self, "Error", "Error al actualizar el producto. Intente de nuevo.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

           