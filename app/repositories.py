from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Barber, Slot


def get_barber(session: Session, barber_id: str) -> Barber | None:
    return session.get(Barber, barber_id)


def list_slots_between(session: Session, barber_id: str, start: datetime, end: datetime) -> list[Slot]:
    query = (
        select(Slot)
        .where(Slot.barber_id == barber_id, Slot.starts_at >= start, Slot.starts_at < end)
        .order_by(Slot.starts_at)
    )
    return list(session.scalars(query))