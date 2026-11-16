from fastapi import FastAPI, HTTPException

app = FastAPI(title="ChairTime")

BARBERS = {
    "marco": "Marco",
    "lea": "Lea",
}

SLOTS = [
    {"id": "sl_1", "barber_id": "marco", "starts_at": "2026-10-17T10:00", "status": "open"},
    {"id": "sl_2", "barber_id": "marco", "starts_at": "2026-10-17T10:30", "status": "booked"},
    {"id": "sl_3", "barber_id": "marco", "starts_at": "2026-10-18T10:00", "status": "open"},
    {"id": "sl_4", "barber_id": "lea", "starts_at": "2026-10-17T10:00", "status": "open"},
]

@app.get("/health/live")
def live():
    return {"status": "ok"}

@app.get("/barbers/{barber_id}/slots")
def list_slots(barber_id: str, date: str):
    if barber_id not in BARBERS:
        raise HTTPException(status_code=404, detail="Barber not found")
    result = []
    for slot in SLOTS:
        if slot["barber_id"]== barber_id and slot["starts_at"].startswith(date):
            result.append(slot)
    return {"items": result}