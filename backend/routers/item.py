from fastapi import APIRouter, HTTPException
from typing import Union, List, Literal
from pydantic import BaseModel
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient, ASCENDING
from geopy import distance

router = APIRouter(
        prefix="/item",
        tags=["item"]
        )

client = MongoClient("127.0.0.1:27017")
db = client.API

class item_add_ret(BaseModel):
    item_id: str

@router.get("/add", response_model=item_add_ret)
def item_add(
        user_id: Union[str, None] = None,
        name: Union[str, None] = None,
        expiry: Union[int, None] = None,
        quantity: Union[int, None] = None
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="user_id is invalid")
    if name == None:
        raise HTTPException(status_code=400, detail="name is invalid")
    if expiry == None or expiry>=0x3afff44180:
        raise HTTPException(status_code=400, detail="expiry is invalid")
    if quantity == None or quantity<=0:
        raise HTTPException(status_code=400, detail="quantity is invalid")
    usr = db.users.find_one({
        "_id": ObjectId(user_id)
        })
    if not usr:
        raise HTTPException(status_code=400, detail="user_id is invalid")
    item = db.items.insert_one({
        "user_id": user_id,
        "name": name,
        "expiry": datetime.fromtimestamp(expiry),
        "quantity": quantity
        })
    return {"item_id": str(item.inserted_id)}

class item_list_ret(BaseModel):
    item_id: str
    name: str
    expiry: int
    address: str
    unit_number: str

@router.get("/list", response_model=List[item_list_ret])
def item_list( 
        sort: Literal["id", "self", "distance", "expiry", "none"] = None,
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None,
        limit: Union[int, None] = 10
        ):
    t = datetime.now()
    res = []
    f = lambda i,u: {
            "item_id":str(i["_id"]),
            "name":i["name"],
            "expiry":i["expiry"].timestamp(),
            "address": u["address"],
            "unit_number": u["unit_number"]
            }
    if sort == "id":
        if item_id == None or not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="item_id is invalid")
        item = db.items.find_one({
            "_id": ObjectId(item_id)
            })
        if not item:
            raise HTTPException(status_code=400, detail="item_id is invalid")
        usr = db.users.find_one({
            "_id": ObjectId(item["user_id"])
            })
        return [f(item,usr)]
    if sort == "self":
        if user_id == None or not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="user_id is invalid")
        usr = db.users.find_one({
            "_id": ObjectId(user_id)
            })
        return [f(i,usr) for i in db.items.find({"user_id":user_id},limit=limit)]
    if sort == "distance":
        if user_id == None or not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="user_id is invalid")
        usr = db.users.find_one({
            "_id": ObjectId(user_id)
            })
        usrs = list(db.users.find({}))
        usrs.sort(key=lambda u:distance.distance(u["point"],usr["point"]))
        ret = []
        for i in usrs[1:]:
            if len(ret)>=limit: break
            ret += [f(j,i) for j in db.items.find({"user_id":str(i["_id"])},limit=limit-len(ret))]
        return ret
    if sort == "expiry":
        usrs = {str(i["_id"]):{"address": i["address"]} for i in db.users.find({})}
        return [f(i,usrs[i["user_id"]]) for i in db.items.find({},limit=limit).sort([("expiry", ASCENDING)])]
    if sort == "none":
        usrs = {str(i["_id"]):i for i in db.users.find({})}
        return [f(i,usrs[i["user_id"]]) for i in db.items.find({},limit=limit)]
    raise HTTPException(status_code=400, detail="Unknown sort")

@router.get("/delete", response_model=bool)
def item_delete(
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="user_id is invalid")
    if item_id == None or not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="item_id is invalid")
    return db.items.delete_one({
        "_id": ObjectId(item_id),
        "user_id": user_id
        }).deleted_count

@router.get("/listingAccept", response_model=bool)
def item_accept(
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="user_id is invalid")
    if item_id == None or not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="item_id is invalid")
    usr = db.users.find_one({
        "_id": ObjectId("user_id")
        })
    if not usr:
        raise HTTPException(status_code=400, detail="usr_id is invalid")
    item = db.items.find_one({
        "_id": ObjectId(item_id)
        })
    if not item:
        raise HTTPException(status_code=400, detail="item_id is invalid")
    raise HTTPException(status_code=501, detail="NotImplementedError")

@router.get("/removeListingAccept", response_model=bool)
def item_unaccept(
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None
        ):
    if user_id == None or not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="user_id is invalid")
    if item_id == None or not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="item_id is invalid")
    usr = db.users.find_one({
        "_id": ObjectId("user_id")
        })
    if not usr:
        raise HTTPException(status_code=400, detail="usr_id is invalid")
    item = db.items.find_one({
        "_id": ObjectId(item_id)
        })
    if not item:
        raise HTTPException(status_code=400, detail="item_id is invalid")
    raise HTTPException(status_code=501, detail="NotImplementedError")
