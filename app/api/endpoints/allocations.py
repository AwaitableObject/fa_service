from typing import Dict

from fastapi import APIRouter, HTTPException
from starlette import status

from app.adapters import orm
from app.domain.exceptions import InvalidSku, OutOfStock
from app.domain.schemas import BatchSchema, OrdeLineScheme
from app.service_layer import services
from app.service_layer.unit_or_work import SqlAlchemyUnitOfWork

orm.start_mappers()
router = APIRouter()


@router.post("/allocation")
def allocate_endpoint(orderline: OrdeLineScheme) -> Dict:
    try:
        batch_ref = services.allocate(
            **orderline.dict(), uow=services.SqlAlchemyUnitOfWork()
        )
    except (OutOfStock, InvalidSku) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    return {"batchref": batch_ref}


@router.post("batch", status_code=status.HTTP_201_CREATED)
def add_batch(batch: BatchSchema) -> Dict:
    services.add_batch(**batch.dict(), uow=SqlAlchemyUnitOfWork())
    return {"batch": batch.dict()}


@router.get("allocation/{orderid}")
def allocations_view_endpoint() -> Dict:
    ...
