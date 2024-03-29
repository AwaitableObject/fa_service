from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import OutOfStock


class Product:
    def __init__(self, sku: str, batches: list[Batch], version_number: int = 0) -> None:
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1

            return batch.reference
        except StopIteration as exc:
            raise OutOfStock(f"Out of stock for sku {line.sku}") from exc


@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, reference: str, sku: str, quantity: int, eta: date | None = None
    ) -> None:
        self.reference: str = reference
        self.sku: str = sku
        self._purchased_quantity: int = quantity
        self.eta: date | None = eta

        self._allocations: set[OrderLine] = set()

    def __repr__(self) -> str:
        return f"<Batch {self.reference}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
