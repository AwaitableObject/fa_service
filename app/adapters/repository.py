from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from app.domain.models import Product
from app.service_layer.interfaces.repository import RepositoryInterface

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session


@dataclass
class SqlAlchemyRepository(RepositoryInterface):
    session: "Session"
    model: Type["Product"] = Product

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> Product | None:
        return self.session.query(self.model).filter_by(sku=sku).first()
