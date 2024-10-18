from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class DetalleCotizacionesView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('system-maxident/ui/historial_cotizacion.ui',self)
