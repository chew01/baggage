from typing import Union
from fastapi import FastAPI
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient
from .routers import items

client = MongoClient("127.0.0.1:27017")
db = client.API

app = FastAPI()

app.include_router(items.router)

@app.get("/")
def ping():
    return {"Hello": "World"}

