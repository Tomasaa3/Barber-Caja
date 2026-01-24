from pathlib import Path
from datetime import datetime
import json

DATA_FILES = Path("data/orders")

def load_summary(date: datetime):
    file = DATA_FILES / str(date.year) / str(date.month) / f"{date.day}.json"
    
    if not file.exists():
        print("summary.py>Todavía no hay datos hoy")
        return
    
    with open(file, "r", encoding="utf-8") as f:
        orders = json.load(f)

    summary = {}

    for order in orders:
        barber = order["barber"]
        if barber not in summary:
            summary[barber] = {
                "se_llevo":0,
                "genero":0,
                "efectivo":0,
                "mercado_pago":0
            }

        summary[barber]["se_llevo"] += (order["service_price"] * (order["barber_comission"]/100)) + order["tip"]
        summary[barber]["genero"] += order["service_price"] * ((100-order["barber_comission"])/100)

        if order["service_payment_method"] == "Efectivo":
            summary[barber]["efectivo"] += order["service_price"]

        if order["service_payment_method"] == "Mercado Pago":
            summary[barber]["mercado_pago"] += order["service_price"] + order["service_recharge"]
    return summary