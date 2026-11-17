from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import jwt
from sqlalchemy.orm import Session

from app import repositories, security
from app.models import Booking, Slot, User

SHOP_TZ = ZoneInfo("America/Toronto")


class NotFound(Exception):
    pass

class InvalidCredentials(Exception):
    pass


class Unauthenticated(Exception):
    pass

class SlotUnavailable(Exception):
    pass


class Forbidden(Exception):
    pass

def list_slots_for_day(session: Session, barber_id: str, day: date):
    if repositories.get_barber(session, barber_id) is None:
        raise NotFound("Barber not found")

    start = datetime.combine(day, time.min, tzinfo=SHOP_TZ)
    end = start + timedelta(days=1)
    return repositories.list_slots_between(session, barber_id, start, end)

def login(session: Session, email: str, password: str) -> str:
    user = repositories.get_user_by_email(session, email)
    if user is None or not security.verify_password(password, user.password_hash):
        raise InvalidCredentials("Wrong email or password")
    return security.create_access_token(user.id, user.role)


def user_from_token(session: Session, token: str) -> User:
    try:
        claims = security.decode_access_token(token)
    except jwt.InvalidTokenError:
        raise Unauthenticated("Invalid or expired token")

    user = repositories.get_user(session, int(claims["sub"]))
    if user is None:
        raise Unauthenticated("Invalid or expired token")
    return user

def book_slot(session: Session, slot_id: int, user: User) -> tuple[Booking, Slot]:
    if user.role != "customer":
        raise Forbidden("Only customers can book for themselves")

    slot = repositories.get_slot(session, slot_id)
    if slot is None:
        raise NotFound("Slot not found")

    if not repositories.claim_slot(session, slot_id):
        session.rollback()
        raise SlotUnavailable("This slot is already booked or blocked")

    booking = repositories.add_booking(session, slot_id, user.id)
    session.commit()
    return booking, slot