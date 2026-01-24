from pathlib import Path
from dataclasses import asdict
import json

DATA_FILE = Path("data/orders")

#Guarda la orden ingresada
def save_order(order):
    date = order.created_at
    folder = DATA_FILE / str(date.year) / str(date.month) / f"{date.day}.json"
    current_order = asdict(order)

    #Si el archivo existe
    if folder.exists():
        print(f"storage.py>Agregando datos a la orden")
        loaded_order = load_orders(folder)
        current_order["created_at"] = current_order["created_at"].isoformat()
        loaded_order.append(current_order)
        with open(folder, "w", encoding="utf-8") as f:
            json.dump(loaded_order, f, indent=4, ensure_ascii=False)
    #Si el archivo no existe
    else:
        print(f"storage.py>No se encontró la orden, creando una nueva...")
        folder.parent.mkdir(parents=True, exist_ok=True)
        current_order["created_at"] = current_order["created_at"].isoformat()
        with open(folder, "w", encoding="utf-8") as f:
            json.dump([current_order], f, indent=4, ensure_ascii=False)

#Carga la orden
def load_orders(path: Path):
    print(f"storage.py>Cargando orden ubicada en: {path}")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return None