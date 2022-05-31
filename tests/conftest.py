from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from app.adapters.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(
    in_memory_db: Engine,  # pylint: disable=W0621
) -> Generator[sessionmaker, None, None]:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory: sessionmaker) -> Session:  # pylint: disable=W0621
    return session_factory()
