from fastapi import APIRouter
from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient
from geopy.geocoders import Nominatim

router = APIRouter(
        prefix="/user",
        tags=["user"]
        )

client = MongoClient("127.0.0.1:27017")
db = client.API

geolocator = Nominatim(user_agent="baggage-backend")

@router.get("/create")
def user_create(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        postal_code: Union[int, None] = None,
        unit_number: Union[str, None] = None):
    if username == None:
        return {"Error": "username is invalid"}
    if password == None:
        return {"Error": "password is invalid"}
    if postal_code == None:
        return {"Error": "postal_code is invalid"}
    if unit_number == None:
        return {"Error": "unit_number is invalid"}
    if db.users.find_one({
        "username": username
        }):
        return {"Error": "User already exists"}
    location = geolocator.geocode({"country":"Singapore","postalcode":postal_code})
    if not location:
        return {"Error": "Cannot find location"}
    usr = db.users.insert_one({
        "username": username,
        "password": password,
        "address": location.address,
        "unit_number": unit_number,
        "point": list(location.point)[:2]
        })
    return {"id": str(usr.inserted_id)}

@router.get("/login")
def user_login(
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
