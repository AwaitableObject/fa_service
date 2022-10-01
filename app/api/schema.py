from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderLineSchema(BaseModel):
    order_id: str
    sku: str
    quantity: int


class BatchSchema(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: Optional[datetime]
