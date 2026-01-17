from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import config

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

def center_label(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    return label
