from fastapi import FastAPI, HTTPException
from .routers import item, user

app = FastAPI()

app.include_router(item.router)
app.include_router(user.router)

@app.get("/")
def ping():
    return {"Hello": "World"}

@app.get("/win")
def win():
    raise HTTPException(status_code=501, detail="NotImplementedError")
