from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import config
from app.adapters.repository import SqlAlchemyRepository

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(config.get_postgres_uri()))


class AbstractUnitOfWork(ABC):  # pragma: no cover
    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory
        self.session: Session
        self.batches: SqlAlchemyRepository

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self.session = self.session_factory()
        self.batches = SqlAlchemyRepository(self.session)

        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        super().__exit__(exc_type, exc_value, traceback)
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
