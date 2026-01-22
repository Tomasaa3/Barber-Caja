from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from ui import components
from logic import storage

class Enter_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window

        #Layout
        self.layout = QtWidgets.QHBoxLayout(self)
        
        #Labels
        self.layout.addWidget(components.center_label("Enter ---> Ingresar datos"))
        self.layout.addWidget(components.center_label("Ctrl + Enter ---> Consultar planillas"))
    
    #Focus del mouse y teclado
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    #Eventos del Teclado
    def keyPressEvent(self, event):
    
        #Ctrl+Enter = Consultas
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.window.show_consult_mode_screen()
            return
    
        #Enter = Barberos
        if event.key() == Qt.Key_Return:
            self.window.show_barbers_screen()

        #Testing
        if event.key() == Qt.Key_T:
            barberos = self.window.config
            print(barberos)

class Barbers_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Barberos
        self.barbers = self.window.config["barbers"]

        #Orden
        self.order = self.window.current_order #Orden Actual
        
        #Layouts
        self.layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QHBoxLayout()
        
        #Título
        self.layout.addWidget(components.center_label("-Barberos-"))
        self.layout.addLayout(self.sec_layout)
        
        #Labels por barbero
        num = 1
        for barber in self.barbers:
            self.sec_layout.addWidget(components.center_label(str(num)+"-"+barber))
            num += 1
    
    #Focus del mouse y teclado
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    #Eventos del Teclado
    def keyPressEvent(self, event):
        
        #Escape = Enter Screen
        if event.key() == Qt.Key_Escape:
            self.window.show_enter_screen()
        
        #1, 2, 3... = Selecciona Barbero
        tecla = event.text()
        if tecla.isdigit():
            num = int(tecla)
            if 0 < num < len(self.barbers)+1:
                barber_list = list(self.barbers)
                print(f"Barbero: {barber_list[num-1]}")
                self.order.barber = barber_list[num-1]
                self.window.show_service_payment_method_screen()

class Service_Payment_Method_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Métodos de pago
        self.payment_methods = self.window.config["payment_methods"]
        
        #Orden
        self.order = self.window.current_order
        
        #Layouts
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.third_layout = QtWidgets.QHBoxLayout()

        #Títulos
        self.main_layout.addWidget(components.center_label("-Servicio-"))
        self.main_layout.addLayout(self.sec_layout)
        self.sec_layout.addWidget(components.center_label("Método de pago"))
        self.sec_layout.addLayout(self.third_layout)

        #Métodos de Pago
        num = 1
        for method in self.payment_methods:
            text = str(num) + "-" + method + "\n Recargo: $" + f"{self.payment_methods[method]:,}"
            self.third_layout.addWidget(components.center_label(text))
            num += 1

    #Focus
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()

    #Eventos del Teclado
    def keyPressEvent(self, event):

        #Ctrl + Escape = Enter Screen
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return
        
        #Escape = Pantalla Barberos
        if event.key() == Qt.Key_Escape:
            self.window.show_barbers_screen()

        #Número = Método de Pago
        if event.text().isdigit():
            num = int(event.text())
            if 0 < num <= len(self.payment_methods):
                payment_methods = list(self.payment_methods)
                print(f"Servicio - Método de Pago: {payment_methods[num-1]}")
                print(f"Servicio - Recarga: ${self.payment_methods[payment_methods[num-1]]:,}")
                self.order.service_payment_method = payment_methods[num-1]
                self.order.service_recharge = self.payment_methods[payment_methods[num-1]]
                self.window.show_services_screen() #Pantalla siguiente

class Services_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Servicios
        self.services = self.window.config["services"]

        #Orden y Recarga por Método de Pago
        self.order = self.window.current_order
        self.recharge = self.order.service_recharge

        #Layout y título
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(components.center_label("-Servicio-"))
        self.sec_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.sec_layout)

        #Servicios
        num = 1
        for service in self.services:
            text = str(num) + "-" + service + "\n$" + str(self.services[service]+self.recharge)
            self.sec_layout.addWidget(components.center_label(text))
            num +=1
        self.sec_layout.addWidget(components.center_label(f"1-Personalizado\n+${self.recharge}"))

    #Focus
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    #Eventos del Teclado
    def keyPressEvent(self, event):

        #Ctrl + Escape = Enter Screen
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return
        
        #Escape = Métodos de Pago
        if event.key() == Qt.Key_Escape:
            self.window.show_service_payment_method_screen()
        
        #Número = Seleccionar Servicio
        if event.text().isdigit():
            services = list(self.services)
            num = event.text()
            if 0 < int(num) <= len(services):
                print(f"Servicio - Monto: ${self.services[services[int(num)-1]]+self.recharge:,}")
                print(f"Servicio: {services[int(num)-1]}")
                self.order.service = services[int(num)-1]
                self.order.service_price = self.services[services[int(num)-1]]
                self.window.show_tip_payment_method_screen()
            
            #Personalizado
            if int(event.text()) == len(services)+1:
                self.clear_content()
                self.input = components.InputPrompt("Ingrese el monto:", "number")
                self.input.submitted.connect(self.on_submit)
                self.input.cancelled.connect(self.on_cancel)
                self.sec_layout.addWidget(self.input)
    
    #Limpia todos los labels
    def clear_content(self):
        while self.sec_layout.count():
            item = self.sec_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    #Al aceptar el monto
    def on_submit(self, answer):
        print(f"Servicio - Monto: {answer}")
        print("Servicio: Personalizado")
        self.order.service = "Personalizado"
        self.order.service_price = int(answer)
        self.window.show_tip_payment_method_screen()
    
    #Al cancelar el monto
    def on_cancel(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_service_payment_method_screen()
    
class Tip_Payment_Method_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Métodos de Pago
        self.payment_methods = self.window.config["payment_methods"]

        #Orden
        self.order = self.window.current_order

        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.third_layout = QtWidgets.QHBoxLayout()

        #Títulos
        self.main_layout.addWidget(components.center_label("-Propina-"))
        self.main_layout.addLayout(self.sec_layout)
        self.sec_layout.addWidget(components.center_label("Método de pago"))
        self.sec_layout.addLayout(self.third_layout)

        #Métodos de Pago
        num = 1
        for method in self.payment_methods:
            text = str(num) + "-" + method
            self.third_layout.addWidget(components.center_label(text))
            num += 1
    
    #Focus
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    #Eventos del Teclado
    def keyPressEvent(self, event):
        #Ctrl + Escape = Enter Screen
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.window.show_enter_screen()
            return
        
        #Escape = Servicios
        if event.key() == Qt.Key_Escape:
            self.window.show_services_screen()
            return
        
        #Número = Seleccionar Método de Pago
        if event.text().isdigit():
            num = int(event.text())
            if 0 < num <= len(self.payment_methods):
                payment_methods = list(self.payment_methods)
                print(f"Propina - Método de Pago: {payment_methods[num-1]}")
                self.order.tip_payment_method = payment_methods[num-1]
                self.window.show_tip_screen()

class Tip_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window

        #Orden
        self.order = self.window.current_order

        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.sec_layout = QtWidgets.QVBoxLayout()
        self.main_layout.insertLayout(1, self.sec_layout)
        
        #Título
        self.main_layout.insertWidget(0, components.center_label("-Propina-"))

        #Prompt - Monto
        self.input = components.InputPrompt("Monto:", "number")
        self.input.submitted.connect(self.on_submitted)
        self.input.cancelled.connect(self.on_cancelled)
        self.sec_layout.insertWidget(0, self.input)

    #Al aceptar
    def on_submitted(self, answer):
        print(f"Propina - Monto: ${int(answer):,}")
        self.order.tip = int(answer)
        self.window.show_client_name_screen()
    
    #Al cancelar
    def on_cancelled(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_tip_payment_method_screen()

#Ultima pantalla del loop input
class Client_Name_Screen(QtWidgets.QWidget):            
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window

        #Order
        self.order = self.window.current_order

        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(components.center_label("-Nombre del cliente-"))

        #Prompt - Nombre
        self.input = components.InputPrompt("Ingrese el nombre:", "text")
        self.input.submitted.connect(self.on_subbmit)
        self.input.cancelled.connect(self.on_cancel)
        self.main_layout.addWidget(self.input)

    #Al aceptar
    def on_subbmit(self, answer):
        print(f"Cliente: {answer}\n")
        self.order.client_name = answer
        storage.save_order(self.order)
        self.window.show_enter_screen()
    
    #Al cancelar
    def on_cancel(self, answer):
        if answer:
            self.window.show_enter_screen()
        else:
            self.window.show_tip_screen()

class Config_Barbers_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Barberos
        self.barbers = self.window.config["barbers"]
        
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

    #Carga de Barberos
    def load_barbers(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Barbero", "%"])
        for barber in self.barbers:
            item_barber = QtGui.QStandardItem(barber)
            item_percent = QtGui.QStandardItem(f"% {self.barbers[barber]:,}")
            self.model.appendRow([item_barber, item_percent])
        self.table.setModel(self.model)
    
    #Añadir Barbero
    def add_barber(self):
        popup = components.addBarberDialog(self)
        if popup.exec_() != QtWidgets.QDialog.Accepted:
            return
        barber = popup.name_input.text()
        percent = popup.percent_input.value()

        if not barber or not percent:
            return
        else:
            self.barbers[barber] = percent
            self.load_barbers()

    #Borrar Barbero  
    def del_barber(self):
        sel_item = self.table.currentIndex().data()
        if not sel_item:
            return
        if self.table.currentIndex().column() != 0:
            return
        del self.barbers[sel_item]
        self.load_barbers()

    #Salir
    def exit_barbers(self):
        from logic import config_saver
        config_saver.save_barbers(self.barbers)
        self.window.show_enter_screen()

class Config_Services_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Servicios
        self.services = self.window.config["services"]
        
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
            #Añadir
        add_button = QtWidgets.QPushButton("Añadir")
        add_button.clicked.connect(self.add_service)
        self.button_layout.addWidget(add_button)
            #Borrar
        del_button = QtWidgets.QPushButton("Borrar")
        del_button.clicked.connect(self.del_service)
        self.button_layout.addWidget(del_button)
            #Salir
        exit_b = QtWidgets.QPushButton("Salir")
        exit_b.clicked.connect(self.exit_services)
        self.main_layout.addWidget(exit_b)

    #Cargar Servicios
    def load_services(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Servicio", "Precio"])
        for service in self.services:
            price_int = self.services[service]
            price_str = f"$ {price_int:,}"
            service_header = QtGui.QStandardItem(service)
            price_header = QtGui.QStandardItem(price_str)
            self.model.appendRow([service_header, price_header])
        self.table.setModel(self.model)
    
    #Añadir Servicio
    def add_service(self):
        popup = components.addServiceDialog(self)
        if popup.exec_() != QtWidgets.QDialog.Accepted:
            return
        value = popup.value_input.text().strip()
        service = popup.service_input.text().strip()
        if not value or not service:
            return
        else:
            print(f"Se añadió el servicio: {service} Precio: $ {int(value):,}")
            self.services[service] = int(value)
        self.load_services()

    #Borrar Servicio
    def del_service(self):
        sel_item = self.table.currentIndex().data()
        if not sel_item:
            return
        if self.table.currentIndex().column() != 0:
            return
        print(f"Se borró el servicio: {sel_item}, Precio: $ {self.services[sel_item]:,}")
        del self.services[sel_item]
        self.load_services()
    
    #Salir
    def exit_services(self):
        from logic import config_saver
        config_saver.save_services(self.services)
        self.window.show_enter_screen()

class Config_Payment_Methods_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        #Métodos de Pago
        self.payment_methods = self.window.config["payment_methods"]
        
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

    #Cargar Métodos de Pago
    def load_payment_methods(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Método de Pago", "Recargo"])
        for payment_method in self.payment_methods:
            method = QtGui.QStandardItem(payment_method)
            recharge = QtGui.QStandardItem(f"$ {self.payment_methods[payment_method]}")
            self.model.appendRow([method, recharge])
        self.table.setModel(self.model)

    #Añadir Método de Pago
    def add_payment_method(self):
        popup = components.addPaymentMethod(self)
        if popup.exec_() != QtWidgets.QDialog.Accepted:
            return
        payment_method = popup.f_input.text()
        payment_recharge = popup.s_input.text()

        if payment_method and payment_recharge:
            self.payment_methods[payment_method] = int(payment_recharge)
            self.load_payment_methods()

    #Borrar Método de Pago
    def del_payment_method(self):
        sel_item = self.table.currentIndex().data()
        if not sel_item:
            print("No")
            return
        else:
            if self.table.currentIndex().column() == 1:
                return
            del self.payment_methods[sel_item]
            self.load_payment_methods()
    
    #Salir
    def exit_payment_methods_screen(self):
        from logic import config_saver
        config_saver.save_payment_methods(self.payment_methods)
        self.window.show_enter_screen()

class Consult_Mode_Screen(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.window = main_window
        self.barbers = self.window.config["barbers"]
        
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.barbers_layout = QtWidgets.QHBoxLayout()

        #Label por Barbero
        num = 1
        for barber in self.barbers:
            text = f"{num} - {barber}"
            label = components.center_label(text)
            self.barbers_layout.addWidget(label)
            num += 1
        self.main_layout.addLayout(self.barbers_layout)
    
    #Focus
    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    #Eventos del teclado
    def keyPressEvent(self, event):
        
        #Escape para salir
        if event.key() == Qt.Key_Escape:
            self.window.show_enter_screen()
        
        #Número = Tabla de Barbero
        if event.text().isdigit():
            num = int(event.text())
            if 0 < num <= len(self.barbers):
                #Cargamos una tabla
                self.load_table(num)

    #Cargar Tabla 
    def load_table(self, num):
        #findchild busca una tabla y si no la encuentra devuelve None
        existe = self.findChild(QtWidgets.QTableView)
        if existe:#Si existe una tabla llamamos a la función le pasamos la tabla
            self.table = components.Load_Barber_Table(True, existe, num)
        else:#Si no existe una tabla llamamos a la función y le pasamos None
            self.table = components.Load_Barber_Table(False, None, num)
            self.main_layout.addWidget(self.table)
            