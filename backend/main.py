from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import item, user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item.router)
app.include_router(user.router)

@app.get("/")
def ping():
    return {"Hello": "World"}

@app.get("/win")
def win():
    raise HTTPException(status_code=501, detail="NotImplementedError")
