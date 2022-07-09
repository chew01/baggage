from fastapi import APIRouter
from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient
from geopy import Nominatim


router = APIRouter(
        prefix="/user",
        tags=["user"]
        )

client = MongoClient("127.0.0.1:27017")
db = client.API

geolocator = Nominatim(user_agent="baggage-backend")

@router.post("/create")
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

@router.get("/getUserById")
def getUserById(id: Union[str, None] = None):
    usr = db.users.find_one(
    {
        "_id" : ObjectId(id)
    }
    )
    if usr:
        usr['_id'] = str(usr['_id'])
        return usr
    else:
        return {"Error": "Problem retrieving user"}

@router.put("/updateUser")
def updateUser(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        postal_code: Union[int, None] = None,
        unit_number: Union[str, None] = None,
        id: Union[str, None] = None):
    usr = db.users.find_one({
        "_id": ObjectId(id)
        })
    if usr:
        if username:
            updated = db.users.update_one({"_id": ObjectId(id)}, 
            {"$set":
                {"username": username}
            })
        if password:
            updated = db.users.update_one({"_id": ObjectId(id)}, 
            {"$set":
                {"password": password} 
            })
        if postal_code:
            updated = db.users.update_one({"_id": ObjectId(id)}, 
            {"$set":
                {"postal_code": postal_code} 
            })
        
        if unit_number:
            updated = db.users.update_one({"_id": ObjectId(id)}, 
            {"$set":
                {"unit_number": unit_number} 
            })

        if updated.modified_count > 0 :
            return {"status":"success"}
        else:
            return {"Error": "Error updating user -- fields may have not changed"}
    else:
        return {"Error": "Error retrieving user, id may be incorrect"}

@router.delete('/deleteUser')
def deleteUser(
    id: Union[str, None] = None
):
    status = db.users.delete_one({"_id":ObjectId(id)})
    if status.deleted_count == 1:
        return {"status": "success", "message": "delete success"}
    else:
        return {"Error": "delete fail"}
    

