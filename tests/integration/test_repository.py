from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

from app.domain.models import Batch
from app.repository import SqlAlchemyRepository
from tests.integration.utils import insert_allocation, insert_batch, insert_order_line


def test_repository_save(session: Session) -> None:
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        text('SELECT reference, sku, _purchased_quantity, eta FROM "batches"')
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_repository_get(session: Session) -> None:
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, batch_id="batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku


def test_repository_list(session: Session) -> None:
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, batch_id="batch1")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.list()

    expected = [Batch("batch1", "GENERIC-SOFA", 100, eta=None)]
    assert retrieved == expected
