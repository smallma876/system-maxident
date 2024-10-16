from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

#QMainWindow Es una clase de PyQt5 que proporciona una ventana principal para la aplicación, con un marco que puede contener menús, barras 
# de herramientas, y áreas centrales.
class LoginView(QMainWindow):
#LoginView hereda de QMainWindow, lo que significa que LoginView es una ventana principal que puede usar todas las funcionalidades de
#  QMainWindow.
    def __init__(self):
        #super().__init__(): Llama al constructor de la clase base (QMainWindow) para asegurarse de que la ventana principal se 
        # inicialice correctamente.
        super().__init__()
        uic.loadUi('system-maxident/ui/login.ui',self)