from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app import repositories

SHOP_TZ = ZoneInfo("America/Toronto")


class NotFound(Exception):
    pass


def list_slots_for_day(session: Session, barber_id: str, day: date):
    if repositories.get_barber(session, barber_id) is None:
        raise NotFound("Barber not found")

    start = datetime.combine(day, time.min, tzinfo=SHOP_TZ)
    end = start + timedelta(days=1)
    return repositories.list_slots_between(session, barber_id, start, end)