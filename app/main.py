from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import services
from app.db import get_session
from app.models import User

app = FastAPI(title="ChairTime")
bearer = HTTPBearer()


# NEW: the shape of a login request
class LoginRequest(BaseModel):
    email: str
    password: str


# NEW: finds out who is calling, from their token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session),
) -> User:
    try:
        return services.user_from_token(session, credentials.credentials)
    except services.Unauthenticated as error:
        raise HTTPException(status_code=401, detail=str(error))


@app.get("/health/live")
def live():
    return {"status": "ok"}


# NEW: log in
@app.post("/auth/login")
def login(body: LoginRequest, session: Session = Depends(get_session)):
    try:
        token = services.login(session, body.email, body.password)
    except services.InvalidCredentials as error:
        raise HTTPException(status_code=401, detail=str(error))
    return {"access_token": token, "token_type": "bearer"}


# NEW: who am I? (a quick way to test tokens)
@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}


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