from datetime import datetime
from typing import List, Optional

from app.domain.exceptions import InvalidSku
from app.domain.models import Batch, OrderLine
from app.domain.models import allocate as model_allocation
from app.service_layer.unit_or_work import SqlAlchemyUnitOfWork


def is_valid_sku(sku: str, batches: List[Batch]) -> bool:
    return sku in {batch.sku for batch in batches}


def add_batch(
    reference: str,
    sku: str,
    quantity: int,
    eta: Optional[datetime],
    uow: SqlAlchemyUnitOfWork,
) -> None:
    with uow:
        uow.batches.add(Batch(reference=reference, sku=sku, quantity=quantity, eta=eta))
        uow.commit()


def allocate(order_id: str, sku: str, quantity: int, uow: SqlAlchemyUnitOfWork) -> str:
    line = OrderLine(order_id=order_id, sku=sku, quantity=quantity)

    with uow:
        batches = uow.batches.list()

        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku {line.sku}")

        batchref = model_allocation(line, batches)

        uow.commit()

    return batchref
