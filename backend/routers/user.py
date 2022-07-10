from fastapi import APIRouter, HTTPException
from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient
from geopy import GoogleV3
from passlib.context import CryptContext
from jose import JWTError, jwt
import random
import os

router = APIRouter(
        prefix="/user",
        tags=["user"]
        )

client = MongoClient("127.0.0.1:27017")
db = client.API

geolocator = GoogleV3(api_key=os.environ['API_KEY'],domain="maps.google.com.sg")

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user: str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode = {"user": user, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=400, detail="Invalid JWT token")
    if data["exp"] < datetime.utcnow().timestamp():
        raise HTTPException(status_code=400, detail="JWT token expired")
    return data["user"]

@router.post("/create")
def user_create(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        postal_code: Union[int, None] = None,
        unit_number: Union[str, None] = None):
    if username == None:
        raise HTTPException(status_code=400, detail="username is invalid")
    if password == None:
        raise HTTPException(status_code=400, detail="password is invalid")
    if postal_code == None:
        raise HTTPException(status_code=400, detail="postal_code is invalid")
    if unit_number == None:
        raise HTTPException(status_code=400, detail="unit_number is invalid")
    if db.users.find_one({
        "username": username
        }):
        raise HTTPException(status_code=400, detail="User already exists")
    location = geolocator.geocode({"country":"Singapore","postalcode":postal_code})
    if not location or location.address=="Singapore":
        raise HTTPException(status_code=400, detail="Cannot find location")
    usr = db.users.insert_one({
        "_id": ObjectId(hex(random.randint(0,16**24-1))[2:]),
        "username": username,
        "password": pwd_context.hash(password),
        "address": location.address,
        "unit_number": unit_number,
        "point": list(location.point)[:2]
        })
    return {"token": create_access_token(username)}

@router.get("/login")
def user_login(
        username: Union[str, None] = None,
        password: Union[str, None] = None):
    if username == None:
        raise HTTPException(status_code=400, detail="username is invalid")
    if password == None:
        raise HTTPException(status_code=400, detail="password is invalid")
    usr = db.users.find_one({
        "username": username,
        })
    if usr and pwd_context.verify(password,usr["password"]):
        return {"token": create_access_token(username)}
    else:
        raise HTTPException(status_code=400, detail="Either username or password is incorrect")

@router.put("/getUserById")
def getUserById(
        user_id: Union[str, None] = None):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    usr = db.users.find_one({"_id": ObjectId(user_id)})
    del usr["password"]
    usr["_id"] = str(usr["_id"])
    return usr

@router.put("/updateUser")
def updateUser(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        postal_code: Union[int, None] = None,
        unit_number: Union[str, None] = None,
        token: Union[str, None] = None):
    user = verify_access_token(token)
    if user:
        if username:
            if db.users.find_one({"username": username}):
                raise HTTPException(status_code=400, detail="Username already exsits")
            updated = db.users.update_one({"username":user},
            {"$set":
                {"username": username}
            })
        if password:
            updated = db.users.update_one({"username":user}, 
            {"$set":
                {"password": password} 
            })
        if postal_code:
            location = geolocator.geocode({"country":"Singapore","postalcode":postal_code})
            if not location or location.address=="Singapore":
                raise HTTPException(status_code=400, detail="Cannot find location")
            updated = db.users.update_one({"username": user}, 
            {"$set":
                {"point": list(location.point)[:2]}
            })
        if unit_number:
            updated = db.users.update_one({"username": user}, 
            {"$set":
                {"unit_number": unit_number} 
            })

        if updated.modified_count > 0 :
            return {"status":"success"}
        else:
            raise HTTPException(status_code=400, detail="Error updating user -- fields may have not changed")
    else:
        raise HTTPException(status_code=400, detail="Error retrieving user, user_id may be incorrect")

@router.delete('/deleteUser')
def deleteUser(
    token: Union[str, None] = None
):
    user = verify_access_token(token)
    usr = db.users.find_one({"username": user})
    if not usr:
        raise HTTPException(status_code=400, detail="Cannot find user")
    user_id = str(usr["_id"])
    status = db.users.delete_one({"username": user})
    if status.deleted_count == 1:
        db.items.delete_many({"user_id":user_id})
        db.items.update_many({"accepted":user_id},{"$set":{"accepted":""}})
        return {"status": "success", "message": "delete success"}
    else:
        raise HTTPException(status_code=400, detail="delete fail")
    

