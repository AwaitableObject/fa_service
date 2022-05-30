import pytest

from app.domain.exceptions import OutOfStock
from app.domain.models import allocate
from tests.unit.utils import make_batch_and_line


def test_success_allocation() -> None:
    batch, line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=20, line_quantity=2
    )

    batchref = allocate(line, batches=[batch])

    assert batchref == batch.reference


@pytest.mark.xfail(raises=OutOfStock)
def test_failed_allocation() -> None:
    batch, line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=2, line_quantity=2
    )
    allocate(line, batches=[batch])

    allocate(line, batches=[batch])
