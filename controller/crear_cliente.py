from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QInputDialog, QMessageBox
from model.clientes import Clientes
class CrearClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        layout = QVBoxLayout(self)

        # Crear un formulario con todos los campos
        form_layout = QFormLayout()

        # Campos de edición
        self.nombre_input = QLineEdit(self)
        form_layout.addRow("Nombre:", self.nombre_input)

        self.ruc_dni_input = QLineEdit(self)
        form_layout.addRow("RUC/DNI:", self.ruc_dni_input)

        self.direccion_input = QLineEdit(self)
        form_layout.addRow("Dirección:", self.direccion_input)

        self.telefono_input = QLineEdit(self)
        form_layout.addRow("Teléfono:", self.telefono_input)

        self.agencia_entrega_input = QLineEdit(self)
        form_layout.addRow("Agencia de Entrega:", self.agencia_entrega_input)

        self.forma_entrega_input = QLineEdit(self)
        form_layout.addRow("Forma de Entrega (Agencia/Domicilio):", self.forma_entrega_input)

        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()

        # Botón Aceptar
        self.ok_button = QPushButton("Registrar", self)
        self.ok_button.setFixedSize(170, 40)  # Tamaño del botón
        self.ok_button.clicked.connect(self.registrar_cliente)
        button_layout.addWidget(self.ok_button)

        # Botón Cancelar
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.setFixedSize(170, 40)  # Tamaño del botón
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # Agregar el layout de botones al layout principal
        layout.addLayout(button_layout)

        self.resize(900, 320)

        # Aplicar estilos
        self.setStyleSheet("""
            QDialog {
                background-color: white; /* Fondo blanco */
                width: 900px;
            }
            QLabel {
                color: black;              /* Texto negro en las etiquetas */
                font-size: 20px;           /* Tamaño de letra */
                font-weight: bold;
                background-color: white;
            }
            QLineEdit {
                background-color: #4c4c4c; /* Fondo gris más claro para los campos de texto */
                color: white;              /* Texto blanco en los campos de texto */
                font-size: 16px;           /* Tamaño de letra */
                padding: 5px;
                border: 1px solid #5c5c5c; /* Borde de los campos de texto */
            }
            QPushButton {
                background-color: #004466;    /* Fondo gris oscuro para los botones */
                color: white;              /* Texto blanco en los botones */
                font-size: 16px;           /* Tamaño de letra */
                padding: 5px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #046697;    /* Color más claro cuando se pasa el mouse sobre los botones */
            }
        """)
    def registrar_cliente(self):
        nombre = self.nombre_input.text().strip()
        ruc_dni = self.ruc_dni_input.text().strip()
        direccion = self.direccion_input.text().strip()
        telefono = self.telefono_input.text().strip()
        agencia_entrega = self.agencia_entrega_input.text().strip()
        forma_entrega = self.forma_entrega_input.text().strip()

        # Validar campos
        if not nombre or not ruc_dni or not direccion or not telefono or not agencia_entrega or not forma_entrega:
            QMessageBox.warning(self, "ERROR", "Por favor, completa todos los campos.")
            return
        else:
            nombre = nombre.upper()
        
        # Intentar registrar el cliente
        try:
            Clientes.create(nombre, telefono, direccion, agencia_entrega, ruc_dni, forma_entrega)
            QMessageBox.information(self, "SISTEMA", "¡CLIENTE REGISTRADO CON ÉXITO!")
            self.accept()  # Cierra el diálogo
        except Exception as e:
            QMessageBox.warning(self, "ERROR", str(e))