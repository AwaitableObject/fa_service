from typing import Dict

from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_201_CREATED

from app import config
from app.adapters import orm
from app.adapters.repository import SqlAlchemyRepository
from app.domain import models
from app.domain.schemas import OrdeLineScheme
from app.domain.services import allocate

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
router = APIRouter()


@router.post("/allocation")
def allocate_endpoint(orderline: OrdeLineScheme) -> Dict:
    session = get_session()
    batches = SqlAlchemyRepository(session).list()
    line = models.OrderLine(**orderline.dict())

    batch_ref = allocate(line, batches)

    return {"batchref": batch_ref}


@router.post("batch", status_code=HTTP_201_CREATED)
def add_batch() -> Dict:
    ...


@router.get("allocation/{orderid}")
def allocations_view_endpoint() -> Dict:
    ...
