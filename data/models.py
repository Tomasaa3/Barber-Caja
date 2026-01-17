from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    barber: Optional[str] = None
    client_name: Optional[str] = None

    service_payment_method: Optional[str] = None
    service_price: Optional[int] = None
    service: Optional[str] = None

    tip_payment_method: Optional[str] = None
    tip: Optional[int] = None

    created_at: datetime = datetime.now()
