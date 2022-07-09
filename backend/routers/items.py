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

@router.get("/addItem")
def addItem(
        user_id: Union[str, None] = None,
        name: Union[str, None] = None,
        expiry_date: Union[int, None] = None,
        quantity: Union[int, None] = None,
        ):
    if user_id == None:
        return {"Error": "user_id is invalid"}
    if name == None:
        return {"Error": "name is invalid"}
    if expiry_date == None:
        return {"Error": "expiry_date is invalid"}
    if quantity == None:
        return {"Error": "quantity is invalid"}
    usr = db.users.find_one({
        "_id": ObjectId(user_id)
        })
    if not usr:
        return {"Error": "user_id is invalid"}
    item = db.items.insert_one({
        "user_id": usr["_id"],
        "username": usr["username"],
        "name": name,
        "expiry_date": datetime.fromtimestamp(expiry_date),
        "quantity": quantity
        })
    return {"item_id": str(item.inserted_id)}

@router.get("/listItems")
def listItems(
        ):
    t = datetime.now()
    return [{"name":i["name"],"expiry_date":str(i["expiry_date"]-t)} for i in db.items.find({})]

@router.get("/myItems")
def myItems(
        user_id: Union[str, None] = None,
        ):
    if user_id == None:
        return {"Error": "user_id is invalid"}
    usr = db.users.find_one({
        "_id": ObjectId(user_id)
        })
    if not usr:
        return {"Error": "user_id is invalid"}
    return [{"item_id": str(i["_id"]), "name": i["name"], "expiry_date": i["expiry_date"]} for i in db.items.find({"user_id":usr["_id"]})]
