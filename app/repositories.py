from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Barber, Slot, User


def get_barber(session: Session, barber_id: str) -> Barber | None:
    return session.get(Barber, barber_id)


def list_slots_between(session: Session, barber_id: str, start: datetime, end: datetime) -> list[Slot]:
    query = (
        select(Slot)
        .where(Slot.barber_id == barber_id, Slot.starts_at >= start, Slot.starts_at < end)
        .order_by(Slot.starts_at)
    )
    return list(session.scalars(query))

def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)