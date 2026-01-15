from PyQt5 import QtWidgets
from ui import screens
from ui import topbar
from data import models


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.topbar = topbar.TopBar(self)
        self.setMenuBar(self.topbar)

        self.current_order = None
        self.show_enter_screen()
    
    def show_enter_screen(self):
        self.setCentralWidget(screens.Enter_Screen(self))
    
    def show_barbers_screen(self):
        self.current_order = models.Order()
        self.setCentralWidget(screens.Barbers_Screen(self))
    
    def show_service_payment_method_screen(self):
        self.setCentralWidget(screens.Service_Payment_Method_Screen(self))
    
    def show_services_screen(self):
        self.setCentralWidget(screens.Services_Screen(self))

    def show_tip_payment_method_screen(self):
        self.setCentralWidget(screens.Tip_Payment_Method_Screen(self))
    
    def show_tip_screen(self):
        self.setCentralWidget(screens.Tip_Screen(self))
    
    def show_client_name_screen(self):
        self.setCentralWidget(screens.Client_Name_Screen(self))
    
    def show_config_barbers_screen(self):
        self.setCentralWidget(screens.Config_Barbers_Screen(self))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


#show event
#print("Payment_Metod_Screen: showEvent (hasFocus=", self.hasFocus(), ")")

#en keypressevent
#print("Payment_Metod_Screen: keyPressEvent -> key:", event.key(), " text:'"+event.text()+"' modifiers:", event.modifiers())