from fastapi import APIRouter, HTTPException
from typing import Union, List, Literal, Optional
from pydantic import BaseModel
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient, ASCENDING
from jose import JWTError, jwt
from geopy import distance
import os

router = APIRouter(
        prefix="/item",
        tags=["item"]
        )

client = MongoClient("127.0.0.1:27017")
db = client.API

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"

def verify_access_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=400, detail="Invalid JWT token")
    if data["exp"] < datetime.utcnow().timestamp():
        raise HTTPException(status_code=400, detail="JWT token expired")
    return data["user"]

def get_user(token: str):
    user = verify_access_token(token)
    usr = db.users.find_one({
        "username": user
        })
    if not usr:
        raise HTTPException(status_code=400, detail="Token is invalid")
    return usr

def get_item(item_id: str):
    if item_id == None or not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="item_id is invalid")
    item = db.items.find_one({
        "_id": ObjectId(item_id)
        })
    if not item:
        raise HTTPException(status_code=400, detail="item_id is invalid")
    return item

class item_add_ret(BaseModel):
    item_id: str

@router.get("/add", response_model=item_add_ret)
def item_add(
        token: Union[str, None] = None,
        name: Union[str, None] = None,
        expiry: Union[int, None] = None,
        quantity: Union[int, None] = None
        ):
    usr = get_user(token)
    if name == None:
        raise HTTPException(status_code=400, detail="name is invalid")
    if expiry == None or expiry>=0x3afff44180:
        raise HTTPException(status_code=400, detail="expiry is invalid")
    if quantity == None or quantity<=0:
        raise HTTPException(status_code=400, detail="quantity is invalid")
    item = db.items.insert_one({
        "user_id": str(usr["_id"]),
        "name": name,
        "expiry": datetime.fromtimestamp(expiry),
        "quantity": quantity,
        "accepted": ""
        })
    return {"item_id": str(item.inserted_id)}

class item_list_ret(BaseModel):
    item_id: str
    item_name: str
    expiry: int
    user_name: str
    address: str
    unit_number: str
    accepted: str

@router.get("/list", response_model=List[item_list_ret])
def item_list( 
        sort: Literal["id", "self", "distance", "expiry", "none"] = None,
        token: Union[str, None] = None,
        item_id: Union[str, None] = None,
        limit: Union[int, None] = 10
        ):
    if limit<=0:
        raise HTTPException(status_code=400, detail="limit is invalid")
    res = []
    f = lambda i,u: {
            "item_id":str(i["_id"]),
            "item_name":i["name"],
            "expiry":i["expiry"].timestamp(),
            "user_name": u["username"],
            "address": u["address"],
            "unit_number": u["unit_number"],
            "accepted": i["accepted"]
            }
    if sort == "id":
        item = get_item(item_id)
        usr = get_user(token)
        if item["accepted"] != "" and str(usr["_id"]) not in [item["accepted"],item["user_id"]]:
            raise HTTPException(status_code=400, detail="item has been accepted")
        return [f(item,usr)]
    if sort == "self":
        usr = get_user(token)
        return [f(i,usr) for i in db.items.find({"user_id":str(usr["_id"])},limit=limit)]
    if sort == "distance":
        usr = get_user(token)
        usrs = list(db.users.find({}))
        usrs.sort(key=lambda u:distance.distance(u["point"],usr["point"]))
        ret = []
        for i in usrs[1:]:
            if len(ret)>=limit: break
            ret += [f(j,i) for j in db.items.find({"user_id":str(i["_id"]),"accepted":""},limit=limit-len(ret))]
        return ret
    if sort == "expiry":
        usrs = {str(i["_id"]):i for i in db.users.find({})}
        return [f(i,usrs[i["user_id"]]) for i in db.items.find({},limit=limit).sort([("expiry", ASCENDING)])]
    if sort == "none":
        usrs = {str(i["_id"]):i for i in db.users.find({})}
        return [f(i,usrs[i["user_id"]]) for i in db.items.find({"accepted":""},limit=limit)]
    raise HTTPException(status_code=400, detail="Unknown sort")

@router.get("/delete", response_model=bool)
def item_delete(
        token: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    usr = get_user(token)
    item = get_item(item_id)
    return db.items.delete_one({
        "_id": ObjectId(item_id),
        "user_id": str(usr["_id"])
        }).deleted_count

@router.get("/listingAccept", response_model=bool)
def item_accept(
        token: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    usr = get_user(token)
    item = get_item(item_id)
    if item and item["user_id"] == str(usr["_id"]):
        raise HTTPException(status_code=400, detail="Cannot accept own item")
    return db.items.update_one({
        "_id": ObjectId(item_id),
        "accepted":""
        },{"$set":{"accepted":str(usr["_id"])}}).matched_count

@router.get("/removeAccept", response_model=bool)
def item_unaccept(
        token: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    usr = get_user(token)
    item = get_item(item_id)
    if not usr: 
        raise HTTPException(status_code=400, detail="user_id is invalid")
    return db.items.update_one({
        "_id": ObjectId(item_id),
        "accepted":str(usr["_id"])
        },{"$set":{"accepted":""}}).matched_count
