from datetime import datetime, timedelta

from app.domain.models import Batch
from tests.unit.utils import make_batch_and_line


def test_allocation_idempotency() -> None:
    batch, line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=20, line_quantity=2
    )

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 18


def test_allocating_to_a_batch() -> None:
    batch, line = make_batch_and_line(
        sku="SMALL-TABLE", batch_quantity=20, line_quantity=2
    )
    batch.allocate(line)

    assert batch.available_quantity == 18


def test_allocate_greater_than_required() -> None:
    batch, line = make_batch_and_line(
        "ELEGANT-LAMP", batch_quantity=20, line_quantity=2
    )
    assert batch.can_allocate(line) is True


def test_allocate_greater_than_available() -> None:
    batch, line = make_batch_and_line(
        "ELEGANT-LAMP", batch_quantity=20, line_quantity=21
    )
    assert batch.can_allocate(line) is False


def test_deallocate() -> None:
    batch, unallocated_line = make_batch_and_line(
        sku="DECORATIVE-TRINKET", batch_quantity=20, line_quantity=2
    )

    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


def test_allocate_and_deallocate() -> None:
    batch, line = make_batch_and_line(
        sku="ANGULAR-DESK", batch_quantity=20, line_quantity=2
    )

    batch.allocate(line)
    batch.deallocate(line)

    assert batch.available_quantity == 20


def test_batch_eq() -> None:
    batch1 = Batch(reference="batch-ref", sku="sku", quantity=10)
    batch2 = Batch(reference="batch-ref", sku="sku", quantity=10)
    batch3 = Batch(reference="batch-ref2", sku="sku", quantity=10)

    assert batch1 == batch2
    assert batch1 != batch3
    assert batch1 != object()


def test_batch_repr() -> None:
    batch = Batch(reference="batch-ref", sku="sku", quantity=10)

    assert repr(batch) == "<Batch batch-ref>"


def test_batch_gt() -> None:
    batch1 = Batch(reference="batch-ref", sku="sku", quantity=10)
    batch2 = Batch(reference="batch-ref", sku="sku", quantity=10, eta=datetime.now())
    batch3 = Batch(
        reference="batch-ref",
        sku="sku",
        quantity=10,
        eta=datetime.now() - timedelta(days=1),
    )

    assert (batch1 > batch2) is False
    assert (batch2 > batch1) is True
    assert (batch3 < batch2) is True


def test_hash() -> None:
    batch1 = Batch(reference="batch-ref", sku="sku", quantity=10)

    assert hash(batch1) == hash(batch1.reference)
