from typing import List

from app.adapters.repository import SqlAlchemyRepository
from app.domain.exceptions import InvalidSku
from app.domain.models import Batch, OrderLine
from app.domain.models import allocate as model_allocation


def is_valid_sku(sku: str, batches: List[Batch]) -> bool:
    return sku in {batch.sku for batch in batches}


def allocate(line: OrderLine, repo: SqlAlchemyRepository) -> str:
    batches = repo.list()

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batchref = model_allocation(line, batches)
    repo.session.commit()

    return batchref
