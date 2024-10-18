from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QComboBox, QMessageBox
from model.product import Productos
class EditarProductoDialog(QDialog):
    def __init__(self, nombre_actual,idcategoria,precio_actual,stock_actual, parent=None):
        super().__init__(parent)
        # Layout principal
        layout = QVBoxLayout(self)

        # Crear un formulario con todos los campos
        form_layout = QFormLayout()

        # Campos de edición
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setText(nombre_actual)  # Cargar el nombre del producto actual
        form_layout.addRow("Nombre del Producto:", self.nombre_input)

        # Cambiar QLineEdit por QComboBox para la categoría
        self.categoria_input = QComboBox(self)
        self.categoria_input.addItems(["VENTA", "INSUMO"])  # Añadir opciones
        # Seleccionar la categoría actual
        if idcategoria == 1:
            self.categoria_input.setCurrentIndex(0)
        else:
            self.categoria_input.setCurrentIndex(1)
        form_layout.addRow("Categoría:", self.categoria_input)

        self.precio_input = QLineEdit(self)
        self.precio_input.setText(str(precio_actual))  # Cargar el stock actual
        form_layout.addRow("Precio por mayor:", self.precio_input)

        self.stock_input = QLineEdit(self)
        self.stock_input.setText(str(stock_actual))  # Cargar el precio actual
        form_layout.addRow("Stock:", self.stock_input)

        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()

        # Botón Aceptar (Editar)
        self.ok_button = QPushButton("Editar Producto", self)
        self.ok_button.setFixedSize(170, 40)  # Tamaño del botón
        self.ok_button.clicked.connect(self.accept)
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
