from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import services
from app.db import get_session

app = FastAPI(title="ChairTime")


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/barbers/{barber_id}/slots")
def list_slots(
    barber_id: str,
    day: date = Query(alias="date"),
    session: Session = Depends(get_session),
):
    try:
        slots = services.list_slots_for_day(session, barber_id, day)
    except services.NotFound as error:
        raise HTTPException(status_code=404, detail=str(error))

    return {
        "items": [
            {
                "id": slot.id,
                "barber_id": slot.barber_id,
                "starts_at": slot.starts_at.astimezone(services.SHOP_TZ).isoformat(),
                "status": slot.status,
            }
            for slot in slots
        ]
    }