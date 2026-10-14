from fastapi import FastAPI

app = FastAPI(title="ChairTime")

@app.get("/health/live")
def live():
    return {"status": "ok"}