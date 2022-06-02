from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm.session import Session

from app.domain.models import Product


class AbstractRepository(ABC):  # pragma: no cover
    @abstractmethod
    def add(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, sku: str) -> Any:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> Product | None:
        return self.session.query(Product).filter_by(sku=sku).first()
