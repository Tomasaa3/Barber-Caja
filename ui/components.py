#Modulos externos
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from datetime import datetime
from pathlib import Path
#Mis archivos .py
from logic import storage
from logic import summary
import config

DATA_FILES = Path("data/orders")

class InputPrompt(QtWidgets.QWidget):
    submitted = pyqtSignal(str)
    cancelled = pyqtSignal(bool)
    def __init__(self, title, mode = "text"):
        super().__init__()
        self.mode = mode
        self.buffer = ""

        self.layout = QtWidgets.QHBoxLayout(self)

        #Label con el título
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        #Label con el texto a ingresar
        self.input_label = QtWidgets.QLabel(self.buffer)
        self.input_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.input_label)

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ControlModifier:
            self.cancelled.emit(True)
            event.accept()
            return
        
        if event.key() == Qt.Key_Escape:
            self.cancelled.emit(False)
            event.accept()
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.submitted.emit(self.buffer)
            event.accept()
            return
        
        if event.key() == Qt.Key_Backspace:
            self.buffer = self.buffer[:-1]
            self.input_label.setText(self.buffer)
            return

        text = event.text()
        if self.mode == "text":
            self.buffer += text
            self.input_label.setText(self.buffer)
            event.accept()
            return
        if self.mode == "number":
            # Solo números: aceptar solo si el texto es dígito
            if text.isdigit():
                self.buffer += text
                self.input_label.setText(self.buffer)
            event.accept()
            return
        if self.mode == "free":
            # Modo libre - pasar texto tal cual
            self.buffer += text
            self.input_label.setText(self.buffer)
            event.accept()
            return


class addBarberDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Barbero")
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        #Nombre
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.main_layout.addWidget(self.name_input)
        #Porcentaje
        self.percent_input = QtWidgets.QSpinBox()
        self.percent_input.setRange(0, 100)
        self.percent_input.setSuffix(" %")
        self.percent_input.setValue(50)
        self.main_layout.addWidget(self.percent_input)
        #Botones
        self.buttons_layout = QtWidgets.QHBoxLayout()
            #Aceptar
        self.b_accept = QtWidgets.QPushButton("Aceptar")
        self.b_accept.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.b_accept)
            #Cancelar
        self.b_cancel = QtWidgets.QPushButton("Cancelar")
        self.b_cancel.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.b_cancel)
                #Añadir Botones al Layout
        self.main_layout.addLayout(self.buttons_layout)

class addServiceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Servicio")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.button_layout = QtWidgets.QHBoxLayout()
        #Input - Nombre del Servicio
        self.service_input = QtWidgets.QLineEdit()
        self.service_input.setPlaceholderText("Servicio")
        self.main_layout.addWidget(self.service_input)
        #Input - Valor del Servicio
        self.value_input = QtWidgets.QLineEdit()
        self.value_input.setPlaceholderText("Valor del Servicio")
        self.validator = QtGui.QDoubleValidator()
        self.value_input.setValidator(self.validator)
        self.main_layout.addWidget(self.value_input)
        #Botones
        self.main_layout.addLayout(self.button_layout)
                #Aceptar
        self.accept_button = QtWidgets.QPushButton("Aceptar")
        self.accept_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.accept_button)
                #Cancelar
        self.cancel_button = QtWidgets.QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

class addPaymentMethod(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Agregar método de Pago")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.button_layout = QtWidgets.QHBoxLayout()

        #Input - Método de Pago
        self.f_input = QtWidgets.QLineEdit()
        self.f_input.setPlaceholderText("Método de Pago")
        self.main_layout.addWidget(self.f_input)

        #Input - Recargo
        self.s_input = QtWidgets.QLineEdit()
        self.s_input.setPlaceholderText("Recargo")
        self.validator = QtGui.QDoubleValidator()
        self.s_input.setValidator(self.validator)
        self.main_layout.addWidget(self.s_input)

        #Botones
            #Aceptar
        self.accept_b = QtWidgets.QPushButton("Aceptar")
        self.accept_b.clicked.connect(self.accept)
        self.button_layout.addWidget(self.accept_b)
            #Cancelar
        self.cancel_b = QtWidgets.QPushButton("Cancelar")
        self.cancel_b.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_b)

        self.main_layout.addLayout(self.button_layout)

class Load_Barber_Table(QtWidgets.QWidget):
    def __init__(self, exsist: bool, created_table: QtWidgets.QTableView, num_barber: int):
        super().__init__()
        #Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        #Fecha y folder
        date = datetime.now()
        folder = DATA_FILES / str(date.year) / str(date.month) / f"{date.day}.json"
        #Bareros
        barberos = list(config.BARBEROS)
        #Encabezados de la tabla
        headers =[
            "Cliente",
            "N°",
            "Servicio",
            "Precio",
            "$",
            "Propina",
            "$",
            "Hora"
        ]
        #Modelo
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(headers)
        #Carga de ordenes del barbero
        orders = storage.load_orders(folder)
        if orders:
            filtered_orders = [
                o for o in orders if o["barber"] == barberos[num_barber-1]
            ]
            num = 1
            for order in filtered_orders:
                time = order["created_at"]
                time = datetime.fromisoformat(time)
                time = time.strftime("%H:%M:%S")
                row = [
                    QtGui.QStandardItem(order["client_name"]),
                    QtGui.QStandardItem(str(num)),
                    QtGui.QStandardItem(order["service"]),
                    QtGui.QStandardItem(f"${order["service_price"]:,}"),
                    QtGui.QStandardItem(order["service_payment_method"]),
                    QtGui.QStandardItem(f"${order["tip"]:,}"),
                    QtGui.QStandardItem(order["tip_payment_method"]),
                    QtGui.QStandardItem(time)
                ]
                num += 1
                self.model.appendRow(row)

        if exsist: #Si existe una tabla, simplemente cargamos el modelo
            print(f"components.py>Usando la tabla existente para {barberos[num_barber-1]}.")
            created_table.setModel(self.model)
            created_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        else: #Si no existe creamos una tabla, cargamos el modelo.
            print(f"components.py>Creando una nueva tabla para {barberos[num_barber-1]}")
            self.table = QtWidgets.QTableView()
            self.table.setModel(self.model)
            self.table.setFocusPolicy(Qt.NoFocus)
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.main_layout.addWidget(self.table)

class Load_Summary(QtWidgets.QWidget):
    def __init__(self, exist: bool, created_table: QtWidgets.QTableView):
        super().__init__()
        #Layout
        self.main_layout = QtWidgets.QHBoxLayout(self)

        #Fecha
        date = datetime.now()

        #Encabezados de la tabla
        headers = ["Barbero","Se llevó", "Generó", "Efectivo", "Mercado Pago"]

        #Modelo
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(headers)

        summarys = summary.load_summary(date)

        for barber in summarys:
            row = [
                QtGui.QStandardItem(barber),
                QtGui.QStandardItem(f"${summarys[barber]["se_llevo"]:,}"),
                QtGui.QStandardItem(f"${summarys[barber]["genero"]:,}"),
                QtGui.QStandardItem(f"${summarys[barber]["efectivo"]:,}"),
                QtGui.QStandardItem(f"${summarys[barber]["mercado_pago"]:,}")
            ]
            self.model.appendRow(row)            

        if exist:
            print("ACAA")
            created_table.setModel(self.model)
            created_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        else:
            self.table = QtWidgets.QTableView()
            self.table.setModel(self.model)
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.main_layout.addWidget(self.table)

def center_label(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    return label