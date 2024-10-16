from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from model.product import Productos  # Importar el modelo de productos

class RegistrarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        layout = QVBoxLayout(self)

        # Crear un formulario con todos los campos
        form_layout = QFormLayout()

        # Campos de edición
        self.nombre_input = QLineEdit(self)
        form_layout.addRow("Nombre del Producto:", self.nombre_input)

        # Cambiar QLineEdit por QComboBox para la categoría
        self.categoria_input = QComboBox(self)
        self.categoria_input.addItems(["VENTA", "INSUMO"])  # Añadir opciones
        form_layout.addRow("Categoría:", self.categoria_input)

        self.stock_input = QLineEdit(self)
        form_layout.addRow("Stock:", self.stock_input)

        self.precio_input = QLineEdit(self)
        form_layout.addRow("Precio por mayor:", self.precio_input)

        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()

        # Botón Aceptar
        self.ok_button = QPushButton("Registrar", self)
        self.ok_button.setFixedSize(170, 40)  # Tamaño del botón
        self.ok_button.clicked.connect(self.registrar_producto)
        button_layout.addWidget(self.ok_button)

        # Botón Cancelar
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.setFixedSize(170, 40)  # Tamaño del botón
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # Agregar el layout de botones al layout principal
        layout.addLayout(button_layout)

        self.resize(900, 250)

        # Aplicar estilos
        self.setStyleSheet("""
            QDialog {
                background-color: white; /* Fondo blanco */
            }
            QLabel {
                color: black;              /* Texto negro en las etiquetas */
                font-size: 20px;           /* Tamaño de letra */
                font-weight: bold;
                background-color: white;
            }
            QLineEdit {
                background-color: #4c4c4c; /* Fondo gris claro */
                color: white;              /* Texto blanco */
                font-size: 16px;
                padding: 5px;
                border: 1px solid #5c5c5c; /* Borde de los campos */
            }
            QComboBox {
                background-color: #4c4c4c; /* Fondo gris claro */
                color: white;              /* Texto blanco */
                font-size: 16px;
                padding: 5px;
                border: 1px solid #5c5c5c; /* Borde del combobox */
            }
            QPushButton {
                background-color: #004466; /* Fondo gris oscuro */
                color: white;
                font-size: 16px;
                padding: 5px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #046697; /* Fondo más claro al pasar el mouse */
            }
        """)

    def registrar_producto(self):
        try:
            nombre = self.nombre_input.text().upper()
            categoria = self.categoria_input.currentText().upper()  # Obtener el texto seleccionado del QComboBox
            stock = int(self.stock_input.text())
            precio = float(self.precio_input.text()) if categoria == "VENTA" else 0.0

            # Validar si los campos están completos
            if not nombre or not categoria or not stock:
                QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
                return

            # Verificar si ya existe un producto con el mismo nombre
            existing_products = Productos.search_by_name(nombre)
            if existing_products:
                QMessageBox.warning(self, "Producto Duplicado", "Ya existe un producto con ese nombre.")
                return

            # Preguntar al usuario si está seguro de registrar el producto
            confirmacion = QMessageBox.question(
                self, 
                "Confirmar Registro", 
                f"¿Está seguro de que desea registrar el producto '{nombre}'?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirmacion == QMessageBox.No:
                return  # Si el usuario selecciona "No", cancelar la operación

            # Mapear la categoría seleccionada al ID correspondiente
            idcategoria = 1 if categoria == "VENTA" else 2

            # Crear el producto
            Productos.create(nombre, idcategoria, precio, stock)
            QMessageBox.information(self, "Éxito", "¡Producto registrado con éxito!")

            self.accept()  # Cerrar el diálogo después de registrar el producto
        except ValueError:
            QMessageBox.warning(self, "Error de datos", "Por favor, complete todos los campos correctamente.")
