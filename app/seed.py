from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select

from app.db import SessionLocal
from app.models import Barber, Slot, User
from app.security import hash_password

SHOP_TZ = ZoneInfo("America/Toronto")
DAYS = ["2026-11-18", "2026-11-19"]
BARBER_IDS = ["marco", "lea"]
USERS = [
    ("sam@example.com", "sam-password", "customer"),
    ("alex@example.com", "alex-password", "customer"),
    ("desk@example.com", "desk-password", "staff"),
]


def seed():
    session = SessionLocal()
    try:
        if session.get(Barber, "marco"):
            print("Already seeded, nothing to do.")
            return

        session.add_all([Barber(id="marco", name="Marco"), Barber(id="lea", name="Léa")])
        session.flush()

        for day in DAYS:
            for barber_id in BARBER_IDS:
                first = datetime.fromisoformat(f"{day}T10:00").replace(tzinfo=SHOP_TZ)
                for i in range(8):
                    starts_at = first + timedelta(minutes=30 * i)
                    session.add(Slot(barber_id=barber_id, starts_at=starts_at, status="open"))

        session.commit()
        print("Seeded 2 barbers and 32 slots.")
    finally:
        session.close()


def seed_users():
    session = SessionLocal()
    try:
        if session.scalar(select(User).limit(1)):
            print("Users already seeded, nothing to do.")
            return

        for email, password, role in USERS:
            session.add(User(email=email, password_hash=hash_password(password), role=role))

        session.commit()
        print(f"Seeded {len(USERS)} users.")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
    seed_users()