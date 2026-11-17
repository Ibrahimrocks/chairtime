# ChairTime

A booking service for independent barbershops. Online bookings and front-desk
walk-ins share one schedule, and a slot can never be double-booked.
SOEN 387 course project.

**Stack:** Python 3.14 · FastAPI · PostgreSQL 16 (SQLAlchemy + Alembic) · Docker Compose

## Run it

1. Copy the settings template: `cp .env.example .env`
2. Start the database (Docker Desktop must be open): `docker compose up -d`
3. Create a virtual environment and install libraries:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create the tables: `alembic upgrade head`
5. Add demo data: `python -m app.seed`
6. Start the service: `fastapi dev app/main.py`
7. Open the contract and try it: http://127.0.0.1:8000/docs

## Demo accounts

| Email | Password | Role |
|---|---|---|
| sam@example.com | sam-password | customer |
| alex@example.com | alex-password | customer |
| desk@example.com | desk-password | staff |

## Race test

With the service running, race 50 simultaneous bookings for one open slot:

```
python race_test.py <slot_id>
```

Expected: one `201`, forty-nine `409`s, and exactly one confirmed booking.

To reproduce the race without protection, start the service with
`NAIVE_BOOKING=1 fastapi dev app/main.py` and run the test on another slot.

## Status (milestone)

Done: slot listing, login (JWT), booking with concurrency protection,
my bookings, race test.
Coming next: idempotency keys, cancellation, staff walk-ins and blocks,
email reminders through an outbox.