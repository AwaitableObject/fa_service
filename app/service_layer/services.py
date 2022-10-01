from datetime import datetime
from typing import TYPE_CHECKING

from app.domain.exceptions import InvalidSku
from app.domain.models import Batch, OrderLine, Product

if TYPE_CHECKING:
    from app.service_layer.unit_or_work import SqlAlchemyUnitOfWork


def add_batch(
    reference: str,
    sku: str,
    quantity: int,
    eta: datetime | None,
    uow: "SqlAlchemyUnitOfWork",
) -> None:
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(
            Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)
        )
        uow.commit()


def allocate(
    order_id: str, sku: str, quantity: int, uow: "SqlAlchemyUnitOfWork"
) -> str:
    line = OrderLine(order_id=order_id, sku=sku, quantity=quantity)

    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")

        batchref = product.allocate(line)
        uow.commit()

    return batchref
