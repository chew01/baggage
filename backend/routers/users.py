from fastapi import APIRouter
from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient

client = MongoClient("127.0.0.1:27017")
db = client.API

router = APIRouter(
        prefix="/items",
        tags=["items"]
        )

@app.get("/createUser")
def createUser(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        location: Union[int, None] = None):
    if username == None:
        return {"Error": "username is invalid"}
    if password == None:
        return {"Error": "password is invalid"}
    if location == None:
        return {"Error": "location is invalid"}
    if db.users.find_one({
        "username": username
        }):
        return {"Error": "User already exists"}
    usr = db.users.insert_one({
        "username": username,
        "password": password,
        "location": location,
        })
    return {"id": str(usr.inserted_id)}

@app.get("/login")
def login(
        username: Union[str, None] = None,
        password: Union[str, None] = None):
    if username == None:
        return {"Error": "username is invalid"}
    if password == None:
        return {"Error": "password is invalid"}
    usr = db.users.find_one({
        "username": username,
        "password": password,
        })
    if usr:
        return {"id": str(usr["_id"])}
    else:
        return {"Error": "Either username or password is incorrect"}
