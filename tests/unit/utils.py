from datetime import date
from typing import Tuple

from app.domain.models import Batch, OrderLine


def make_batch_and_line(
    sku: str, batch_quantity: int, line_quantity: int
) -> Tuple[Batch, OrderLine]:
    return (
        Batch(
            reference="batch-001", sku=sku, quantity=batch_quantity, eta=date.today()
        ),
        OrderLine(order_id="order-ref", sku=sku, quantity=line_quantity),
    )
