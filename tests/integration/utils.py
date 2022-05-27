from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text


def insert_order_line(session: Session) -> int:
    session.execute(
        text(
            "INSERT INTO order_lines (order_id, sku, quantity)"
            ' VALUES ("order1", "GENERIC-SOFA", 12)'
        )
    )
    [[order_line_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE order_id=:order_id AND sku=:sku"),
        dict(order_id="order1", sku="GENERIC-SOFA"),
    )
    return order_line_id


def insert_batch(session: Session, batch_id: str) -> str:
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)'
        ),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"'),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session: Session, orderline_id: int, batch_id: str) -> None:
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"
        ),
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )
