from pathlib import Path
import json

CONFIG_FILES = Path("config")

def save_barbers(barbers: dict):
    file = CONFIG_FILES / "barbers.json"

    if file.exists():
        print("Guardando Barberos")
        with open(file, "w", encoding="utf-8") as f:
            json.dump(barbers, f, indent=4, ensure_ascii=False)
    else:
        print("Guardando Barberos en un archivo nuevo.")
        file.parent.mkdir(parents=True, exist_ok=True) #Creamos el folder
        with open(file, "w", encoding="utf-8") as f:
            json.dump(barbers, f, indent=4, ensure_ascii=False)

def save_services(services: dict):
    file = CONFIG_FILES / "services.json"

    if file.exists():
        print("Guardando Servicios")
        with open(file, "w", encoding="utf-8") as f:
            json.dump(services, f, indent=4, ensure_ascii=False)
    else:
        print("Guardando Servicios en un archivo nuevo")
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w", encoding="utf-8") as f:
            json.dump(services, f, indent=4, ensure_ascii=False)
    
def save_payment_methods(payment_methods: dict):
    file = CONFIG_FILES / "payment_methods.json"

    if file.exists():
        print("Guardando Métodos de Pago")
        with open(file, "w", encoding="utf-8") as f:
            json.dump(payment_methods, f, indent=4, ensure_ascii=False)
    else:
        print("Guardando Métodos de Pago en un archivo nuevo.")
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w", encoding="utf-8") as f:
            json.dump(payment_methods, f, indent=4, ensure_ascii=False)