from pydantic import BaseModel


class OrdeLineScheme(BaseModel):
    order_id: str
    sku: str
    quantity: int
