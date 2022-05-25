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
