from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from ui import components
import config

class Enter_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(components.center_label("Enter ---> Ingresar datos"))
        self.layout.addWidget(components.center_label("Ctrl + Enter ---> Consultar planillas"))
        self.setFocusPolicy(Qt.StrongFocus)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            print("¡Presionaste Ctrl + Enter!")
            return None

        if event.key() == Qt.Key_Return:
            self.window.show_barbers_screen()

class Barbers_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window

        self.layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(components.center_label("-Barberos-"))
        self.layout.addLayout(self.sec_layout)
        
        num = 1
        for barbero in config.BARBEROS:
            self.sec_layout.addWidget(components.center_label(str(num)+"-"+barbero))
            num += 1

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.window.show_enter_screen()
        
        tecla = event.text()
        if tecla.isdigit():
            num = int(tecla)
            if 0 < num < len(config.BARBEROS)+1:
                print(f"Barbero: {config.BARBEROS[num-1]}")
                #GUARDAR SELECCIÓN 
                self.window.show_service_payment_method_screen()

class Service_Payment_Method_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(components.center_label("-Método de pago del servicio-"))
        self.main_layout.addLayout(self.sec_layout)

        num = 1
        for method in config.METODOS_DE_PAGO:
            text = str(num)+"-"+method ###Agregar aumento por mp
            self.sec_layout.addWidget(components.center_label(text))
            num += 1

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return

        if event.key() == Qt.Key_Escape:
            self.window.show_barbers_screen()

        if event.text().isdigit():
            number = int(event.text())
            if 0 < number <= len(config.METODOS_DE_PAGO):
                self.window.show_services_screen()
                #Guardar selección acá
                print(f"Método de pago: {number}-{config.METODOS_DE_PAGO[number-1]}")

class Services_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(components.center_label("-Servicio-"))
        self.sec_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.sec_layout)

        num = 1
        for service in config.SERVICIOS:
            text = str(num) + "-" + service + "\n$" + str(config.SERVICIOS[service])
            self.sec_layout.addWidget(components.center_label(text))
            num +=1
        self.sec_layout.addWidget(components.center_label(str(num)+"-Personalizado"))

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return
        
        if event.key() == Qt.Key_Escape:
            self.window.show_service_payment_method_screen()
        
        if event.text().isdigit():
            services = list(config.SERVICIOS)
            if 0 < int(event.text()) <= len(services):
                print(event.text())
            
            if int(event.text()) == len(services)+1:
                print(event.text())
                self.clear_content()
                self.input = components.InputPrompt("Ingrese el monto:", "number")
                self.input.submitted.connect(self.on_subbmit)
                self.input.cancelled.connect(self.on_cancel)
                self.sec_layout.addWidget(self.input)
    
    def clear_content(self):
        while self.sec_layout.count():
            item = self.sec_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def on_subbmit(self, answer):
        print(answer)
        self.window.show_tip_screen()
    
    def on_cancel(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_service_payment_method_screen()
    
class Tip_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()

        self.main_layout.insertLayout(1, self.sec_layout)
        self.main_layout.insertWidget(0, components.center_label("-Propina-"))

        self.sec_layout.addWidget(components.center_label("1-Si"))
