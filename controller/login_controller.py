from PyQt5.QtWidgets import QMessageBox ,QLabel ,QLineEdit
from PyQt5.QtCore import Qt
from views.login_view import LoginView
from model.database import get_connection
from controller.ingreso_controller import IngresoController
from controller.menu_controller import MenuWindow
class LoginController:
    def __init__(self):
        self.view = LoginView() # instancia de la clase loginviwe que contiene la imagen del login 
        self.view.loginButton.clicked.connect(self.login) # señales que conectan al boton iniciar y salir
        self.view.cancelButton.clicked.connect(self.cancel)

        self.view.forgot_password_label = self.view.findChild(QLabel, "olvidaste_contrasena")  # Asegúrate de usar el nombre correcto
        self.view.forgot_password_label.mousePressEvent = self.show_password_recovery  # Conecta el evento

        self.view.txtUsuario.keyPressEvent = self.create_keypress_handler(self.view.txtUsuario.keyPressEvent)
        self.view.txtContrasea.keyPressEvent = self.create_keypress_handler(self.view.txtContrasea.keyPressEvent)
    def cancel(self):
        self.view.close()

    def login(self):
        
        username = self.view.txtUsuario.text()
        password = self.view.txtContrasea.text()
        if self.authenticate(username, password):
            
            QMessageBox.information(self.view, "LOGIN","BIENVENIDO A MAXIDENT!",QMessageBox.Ok)
            self.view.close()  
            self.show_menu()  

        else:
            QMessageBox.warning(self.view, "Login","Revisa tus datos!!",QMessageBox.Ok)

    def authenticate(self, username, password):
        conn = get_connection()
        #Creas un cursor a partir de la conexión. El cursor es esencial para ejecutar comandos SQL y recuperar resultados. Es un objeto que 
        #  permite interactuar con la base de dato
        cursor = conn.cursor()
        #Aquí, el símbolo ? actúa como un marcador de posición. Significa que se debe reemplazar por el valor real del nombre de 
        # usuario que el usuario introdujo en el formulario de inicio de sesión.
        cursor.execute("SELECT Username,Password FROM Users WHERE Username=? AND Password=?", (username, password))
        #El uso de fetchone() en tu código te permite determinar si un usuario con las credenciales proporcionadas existe en la base de datos.
        user = cursor.fetchone()
        conn.close()
        return user is not None
    
    def show_menu(self):
        self.menu_controller=MenuWindow()
        self.menu_controller.view.show()
    
    def show_password_recovery(self, event):
        # Aquí puedes abrir una nueva ventana o lanzar un proceso para restablecer la contraseña
        QMessageBox.information(self.view,"Recuperación de Contraseña", "Llamar al numero de soporte 969613558")
    
    def create_keypress_handler(self, original_keyPressEvent):
        # Este método crea un manejador personalizado para el evento de keypress sin bloquear el comportamiento original
        def keypress_event(event):
            if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.login()  # Llamar a la función login cuando se presiona Enter
            else:
                original_keyPressEvent(event)  # Pasar el evento al método original para que funcione como un campo de texto normal
        return keypress_event