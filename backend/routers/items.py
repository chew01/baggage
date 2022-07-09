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

@router.get("/add")
def addItem(
        user_id: Union[str, None] = None,
        name: Union[str, None] = None,
        expiry_date: Union[int, None] = None,
        quantity: Union[int, None] = None,
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        return {"Error": "user_id is invalid"}
    if name == None:
        return {"Error": "name is invalid"}
    if expiry_date == None:
        return {"Error": "expiry_date is invalid"}
    if quantity == None or quantity<=0:
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

@router.get("/list")
def listItems(
        sort: Union[str, None] = None,
        item_id: Union[str, None] = None,
        limit: Union[int, None] = 25
        ):
    t = datetime.now()
    res = []
    return res
    return [{"name":i["name"],"expiry_date":str(i["expiry_date"]-t)} for i in db.items.find({})]

@router.get("/self")
def myItems(
        user_id: Union[str, None] = None,
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        return {"Error": "user_id is invalid"}
    usr = db.users.find_one({
        "_id": ObjectId(user_id)
        })
    if not usr:
        return {"Error": "user_id is invalid"}
    return [{"item_id": str(i["_id"]), "name": i["name"], "expiry_date": i["expiry_date"]} for i in db.items.find({"user_id":usr["_id"]})]

@router.get("/delete")
def myItems(
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        return {"Error": "user_id is invalid"}
    if item_id == None or not ObjectId.is_valid(item_id):
        return {"Error": "item_id is invalid"}
    if db.items.delete_one({
        "_id": ObjectId(item_id),
        "user_id": ObjectId(user_id)
        }).deleted_count:
        return {"Success": "Item deleted"}
    return {"Error": "Could not delete item"}
