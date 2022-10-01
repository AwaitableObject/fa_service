from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domain.models import Product


class RepositoryInterface(Protocol):
    @abstractmethod
    def add(self, product: "Product") -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, sku: str) -> "Product" | None:
        raise NotImplementedError
