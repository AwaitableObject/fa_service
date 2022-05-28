from typing import Dict

from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.post("allocate")
def allocate_endpoint() -> Dict:
    ...


@router.post("batch", status_code=HTTP_201_CREATED)
def add_batch() -> Dict:
    ...


@router.get("allocations/{orderid}")
def allocations_view_endpoint() -> Dict:
    ...
