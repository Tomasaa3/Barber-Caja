from PyQt5 import QtWidgets

class TopBar(QtWidgets.QMenuBar):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self._build()
    
    def _build(self):
        #Archivo
        file_menu = self.addMenu("Archivo")

        #Configuración
        config_menu = self.addMenu("Configuración")
                #Barberos
        barbers_action = QtWidgets.QAction("Barberos", self)
        barbers_action.triggered.connect(self.window.show_config_barbers_screen)
        config_menu.addAction(barbers_action)
                #Servicios
        service_action = QtWidgets.QAction("Servicios", self)
        service_action.triggered.connect(self.window.show_config_services_screen)
        config_menu.addAction(service_action)
                #Métodos de Pago
        payment_methods_action = QtWidgets.QAction("Métodos de Pago", self)
        payment_methods_action.triggered.connect(self.window.show_config_payment_methods_screen)
        config_menu.addAction(payment_methods_action)