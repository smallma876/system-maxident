from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('system-maxident/ui/menu.ui',self)

 