import pytest
from sqlalchemy.orm import sessionmaker

from app.service_layer.unit_or_work import SqlAlchemyUnitOfWork
from tests.integration.utils import insert_batch


def test_uow_commit(session_factory: sessionmaker) -> None:
    uow = SqlAlchemyUnitOfWork(session_factory)

    with uow:
        insert_batch(uow.session, "batch1")
        uow.commit()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert len(rows) == 1


def test_uow_rollback(session_factory: sessionmaker) -> None:
    uow = SqlAlchemyUnitOfWork(session_factory)

    with uow:
        insert_batch(uow.session, "batch1")

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert not rows


def test_uow_rollback_on_error(session_factory: sessionmaker) -> None:
    class TestException(Exception):
        ...

    uow = SqlAlchemyUnitOfWork(session_factory)

    with pytest.raises(TestException):
        with uow:
            insert_batch(uow.session, "batch1")
            raise TestException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert not rows
