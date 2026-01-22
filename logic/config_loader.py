from pathlib import Path
import json

CONFIG_FILES = Path("config")

def load_all_configs():
    #Esta funcion debería ejecutar load_barber, load_services y load_payment_methods y devolver un diccionario así
    configuraciones = {}
    configuraciones["barbers"] = load_barbers()
    configuraciones["services"] = load_services()
    configuraciones["payment_methods"] = load_payment_methods()
    return configuraciones

#Estas 3 funciones deberían cargar un json y devolver su contenido en formato dict.
def load_barbers():
    file = CONFIG_FILES / "barbers.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            barbers = json.load(f)
        return barbers
    else:
        return {}

def load_services():
    file = CONFIG_FILES / "services.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            services = json.load(f)
        return services
    else:
        return {}
    
def load_payment_methods():
    file = CONFIG_FILES / "payment_methods.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            payment_methods = json.load(f)
        return payment_methods
    else:
        return {}