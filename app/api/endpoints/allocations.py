from typing import Dict

from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from app import config
from app.adapters import orm
from app.adapters.repository import SqlAlchemyRepository
from app.domain import models
from app.domain.exceptions import InvalidSku, OutOfStock
from app.domain.schemas import OrdeLineScheme
from app.service_layer.services import allocate

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
router = APIRouter()


@router.post("/allocation")
def allocate_endpoint(orderline: OrdeLineScheme) -> Dict:
    session = get_session()
    repository = SqlAlchemyRepository(session)
    line = models.OrderLine(**orderline.dict())

    try:
        batch_ref = allocate(line, repository)
    except (OutOfStock, InvalidSku) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    return {"batchref": batch_ref}


@router.post("batch", status_code=status.HTTP_201_CREATED)
def add_batch() -> Dict:
    ...


@router.get("allocation/{orderid}")
def allocations_view_endpoint() -> Dict:
    ...
