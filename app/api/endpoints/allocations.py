from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException
from starlette import status

from app.adapters import orm
from app.domain.exceptions import InvalidSku, OutOfStock
from app.service_layer import services
from app.service_layer.unit_or_work import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from app.api.schema import BatchSchema, OrderLineSchema

orm.start_mappers()
router = APIRouter()


@router.post("/allocation")
def allocate_endpoint(orderline: "OrderLineSchema") -> dict:
    try:
        batch_ref = services.allocate(
            **orderline.dict(), uow=services.SqlAlchemyUnitOfWork()
        )
    except (OutOfStock, InvalidSku) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    return {"batchref": batch_ref}


@router.post("batch", status_code=status.HTTP_201_CREATED)
def add_batch(batch: "BatchSchema") -> dict:
    services.add_batch(**batch.dict(), uow=SqlAlchemyUnitOfWork())
    return {"batch": batch.dict()}


@router.get("allocation/{orderid}")
def allocations_view_endpoint() -> dict:
    ...
