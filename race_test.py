import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import httpx
from sqlalchemy import func, select

from app.db import SessionLocal
from app.models import Booking

BASE_URL = "http://127.0.0.1:8000"
REQUESTS = 50


def login(email: str, password: str) -> str:
    response = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()["access_token"]


def main():
    slot_id = int(sys.argv[1])
    tokens = [
        login("sam@example.com", "sam-password"),
        login("alex@example.com", "alex-password"),
    ]
    start_line = threading.Barrier(REQUESTS)

    def attempt(i: int) -> int:
        token = tokens[i % 2]
        start_line.wait()
        response = httpx.post(
            f"{BASE_URL}/slots/{slot_id}/bookings",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        return response.status_code

    with ThreadPoolExecutor(max_workers=REQUESTS) as pool:
        codes = list(pool.map(attempt, range(REQUESTS)))

    print("Status codes:", dict(Counter(codes)))

    with SessionLocal() as session:
        confirmed = session.scalar(
            select(func.count())
            .select_from(Booking)
            .where(Booking.slot_id == slot_id, Booking.status == "confirmed")
        )
    print(f"Confirmed bookings for slot {slot_id}: {confirmed}")


if __name__ == "__main__":
    main()