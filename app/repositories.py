import time
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import Barber, Booking, Slot, User


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

def get_slot(session: Session, slot_id: int) -> Slot | None:
    return session.get(Slot, slot_id)


def claim_slot(session: Session, slot_id: int) -> bool:
    result = session.execute(
        update(Slot)
        .where(Slot.id == slot_id, Slot.status == "open")
        .values(status="booked")
    )
    return result.rowcount == 1


def add_booking(session: Session, slot_id: int, customer_id: int) -> Booking:
    booking = Booking(slot_id=slot_id, customer_id=customer_id, status="confirmed")
    session.add(booking)
    session.flush()
    return booking

def claim_slot_naive(session: Session, slot_id: int) -> bool:
    slot = session.get(Slot, slot_id)
    if slot.status != "open":
        return False
    time.sleep(0.05)
    slot.status = "booked"
    session.flush()
    return True

def list_bookings_for_customer(session: Session, customer_id: int) -> list:
    query = (
        select(Booking, Slot)
        .join(Slot, Booking.slot_id == Slot.id)
        .where(Booking.customer_id == customer_id, Booking.status == "confirmed")
        .order_by(Slot.starts_at)
    )
    return list(session.execute(query).all())