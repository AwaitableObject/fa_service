from typing import List

from app.domain.exceptions import OutOfStock
from app.domain.models import Batch, OrderLine


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in batches if b.can_allocate(line))
        batch.allocate(line)

        return batch.reference
    except StopIteration as e:
        raise OutOfStock(f"Out of stock for sku {line.sku}") from e
