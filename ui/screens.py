from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
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
        if event.key() == Qt.Key_Return:
            self.window.show_barbers_screen()

class Barbers_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order #Orden Actual

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
                barber_list = list(config.BARBEROS)
                print(f"Barbero: {barber_list[num-1]}")
                self.order.barber = barber_list[num-1]
                self.window.show_service_payment_method_screen() #Pantalla siguiente

class Service_Payment_Method_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.third_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(components.center_label("-Servicio-"))
        self.main_layout.addLayout(self.sec_layout)
        self.sec_layout.addWidget(components.center_label("Método de pago"))
        self.sec_layout.addLayout(self.third_layout)

        num = 1
        for method in config.METODOS_DE_PAGO:
            text = str(num) + "-" + method
            self.third_layout.addWidget(components.center_label(text))
            num += 1

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen() #Volver al inicio
            return

        if event.key() == Qt.Key_Escape:
            self.window.show_barbers_screen() #Pantalla anterior

        if event.text().isdigit():
            num = int(event.text())
            if 0 < num <= len(config.METODOS_DE_PAGO):
                payment_methods = list(config.METODOS_DE_PAGO)
                print(f"Servicio - Método de Pago: {payment_methods[num-1]}")
                self.order.service_payment_method = payment_methods[num-1]
                self.window.show_services_screen() #Pantalla siguiente

class Services_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order

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
            num = event.text()
            if 0 < int(num) <= len(services):
                print(f"Servicio - Monto: ${config.SERVICIOS[services[int(num)-1]]}")
                print(f"Servicio: {services[int(num)-1]}")
                self.order.service = services[int(num)-1]
                self.order.service_price = config.SERVICIOS[services[int(num)-1]]
                self.window.show_tip_payment_method_screen()
            
            if int(event.text()) == len(services)+1:
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
        print(f"Servicio - Monto: {answer}")
        print("Servicio: Personalizado")
        self.order.service = "Personalizado"
        self.order.service_price = answer
        self.window.show_tip_payment_method_screen()
    
    def on_cancel(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_service_payment_method_screen()
    
class Tip_Payment_Method_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.third_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(components.center_label("-Propina-"))
        self.main_layout.addLayout(self.sec_layout)
        self.sec_layout.addWidget(components.center_label("Método de pago"))
        self.sec_layout.addLayout(self.third_layout)

        num = 1
        for method in config.METODOS_DE_PAGO:
            text = str(num) + "-" + method
            self.third_layout.addWidget(components.center_label(text))
            num += 1
        
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return
        
        if event.key() == Qt.Key_Escape:
            self.window.show_services_screen()
            return
        
        if event.text().isdigit():
            num = int(event.text())
            if 0 < num <= len(config.METODOS_DE_PAGO):
                payment_methods = list(config.METODOS_DE_PAGO)
                print(f"Propina - Método de Pago: {payment_methods[num-1]}")
                self.order.tip_payment_method = payment_methods[num-1]
                self.window.show_tip_screen()

class Tip_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.main_layout.insertLayout(1, self.sec_layout)
        
        self.main_layout.insertWidget(0, components.center_label("-Propina-"))

        self.input = components.InputPrompt("Monto:", "number")
        self.input.submitted.connect(self.on_submitted)
        self.input.cancelled.connect(self.on_cancelled)
        self.sec_layout.insertWidget(0, self.input)

    def on_submitted(self, answer):
        print(f"Propina - Monto: {answer}")
        self.order.tip = int(answer)
        self.window.show_client_name_screen()
    
    def on_cancelled(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_tip_payment_method_screen()

class Client_Name_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.order = self.window.current_order

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(components.center_label("-Nombre del cliente-"))

        self.input = components.InputPrompt("Ingrese el nombre:", "text")
        self.input.submitted.connect(self.on_subbmit)
        self.input.cancelled.connect(self.on_cancel)
        self.main_layout.addWidget(self.input)

    def on_subbmit(self, answer):
        print(f"Cliente: {answer}\n\n")
        self.order.client_name = answer
        print(self.order)
        self.window.show_enter_screen()
    
    def on_cancel(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_tip_screen()

class Config_Barbers_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.sec_layout)
        self.button_layout = QtWidgets.QVBoxLayout()

        #Modelo
        self.model = QtGui.QStandardItemModel()

        #Tabla
        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().setVisible(False)
        self.load_barbers()
        self.sec_layout.addWidget(self.table)

        #Botones
        self.sec_layout.addLayout(self.button_layout)
            #Añadir
        self.add_b = QtWidgets.QPushButton("Añadir")
        self.add_b.clicked.connect(self.add_barber)
        self.button_layout.addWidget(self.add_b)
            #Borrar
        self.del_b = QtWidgets.QPushButton("Borrar")
        self.del_b.clicked.connect(self.del_barber)
        self.button_layout.addWidget(self.del_b)
            #Salir
        self.exit_b = QtWidgets.QPushButton("Salir")
        self.exit_b.clicked.connect(self.exit_barbers)
        self.main_layout.addWidget(self.exit_b)

    def load_barbers(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Barbero", "%"])
        for barber in config.BARBEROS:
            item_barber = QtGui.QStandardItem(barber)
            item_percent = QtGui.QStandardItem(f"% {config.BARBEROS[barber]:,}")
            self.model.appendRow([item_barber, item_percent])
        self.table.setModel(self.model)

    def add_barber(self):
        popup = components.addBarberDialog(self)
        if popup.exec_() != QtWidgets.QDialog.Accepted:
            return
        barber = popup.name_input.text()
        percent = popup.percent_input.value()

        if not barber or not percent:
            return
        else:
            config.BARBEROS[barber] = percent
            self.load_barbers()
        
    def del_barber(self):
        sel_item = self.table.currentIndex().data()
        if not sel_item:
            return
        else:
            del config.BARBEROS[sel_item]
            self.load_barbers()

    def exit_barbers(self):
        self.window.show_enter_screen()

class Config_Services_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.sec_layout)
        self.button_layout = QtWidgets.QVBoxLayout()

        #Tabla
        self.model = QtGui.QStandardItemModel()
        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().setVisible(False)
        self.load_services() #Carga de datos
        self.sec_layout.addWidget(self.table)
        self.sec_layout.addLayout(self.button_layout)
    
        #Botones
        add_button = QtWidgets.QPushButton("Añadir")
        add_button.clicked.connect(self.add_service)
        self.button_layout.addWidget(add_button)

        del_button = QtWidgets.QPushButton("Borrar")
        del_button.clicked.connect(self.del_service)
        self.button_layout.addWidget(del_button)

        exit_b = QtWidgets.QPushButton("Salir")
        exit_b.clicked.connect(self.exit_services)
        self.main_layout.addWidget(exit_b)

    def load_services(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Servicio", "Precio"])
        for service in config.SERVICIOS:
            price_int = config.SERVICIOS[service]
            price_str = f"$ {price_int:,}"
            service_header = QtGui.QStandardItem(service)
            price_header = QtGui.QStandardItem(price_str)
            self.model.appendRow([service_header, price_header])
        self.table.setModel(self.model)
    
    def add_service(self):
        popup = components.addServiceDialog(self)
        if popup.exec_() != QtWidgets.QDialog.Accepted:
            return
        value = popup.value_input.text().strip()
        service = popup.service_input.text().strip()
        if not value or not service:
            return
        else:
            print(f"Se añadió el servicio: {service} Precio: ${int(value):,}")
            config.SERVICIOS[service] = int(value)
        self.load_services()

    def del_service(self):
        sel_item = self.table.currentIndex().data()
        del config.SERVICIOS[sel_item]
        self.load_services()
    
    def exit_services(self):
        self.window.show_enter_screen()

class Config_Payment_Methods_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.sec_layout)
        #Modelo
        self.model = QtGui.QStandardItemModel()
        #Tabla
        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().setVisible(False)
        self.load_payment_methods()
        self.sec_layout.addWidget(self.table)
        #Botones
            #Añadir
        self.add_b = QtWidgets.QPushButton("Añadir")
        self.add_b.clicked.connect(self.add_payment_method)
        self.button_layout.addWidget(self.add_b)
            #Borrar
        self.del_b = QtWidgets.QPushButton("Borrar")
        self.del_b.clicked.connect(self.del_payment_method)
        self.button_layout.addWidget(self.del_b)
            #Salir
        self.exit_b = QtWidgets.QPushButton("Salir")
        self.exit_b.clicked.connect(self.exit_payment_methods_screen)
        self.main_layout.addWidget(self.exit_b)
        self.sec_layout.addLayout(self.button_layout)

    def load_payment_methods(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Método de Pago", "Recargo"])
        for payment_method in config.METODOS_DE_PAGO:
            method = QtGui.QStandardItem(payment_method)
            recharge = QtGui.QStandardItem(f"$ {config.METODOS_DE_PAGO[payment_method]:,}")
            self.model.appendRow([method, recharge])
        self.table.setModel(self.model)

    def add_payment_method(self):
        print("AÑADIR")
    def del_payment_method(self):
        sel_item = self.table.currentIndex().data()
    def exit_payment_methods_screen(self):
        self.window.show_enter_screen()