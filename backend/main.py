from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta

client = MongoClient("127.0.0.1:27017")
db=client.API

app = FastAPI()

@app.get("/")
def ping():
    return {"Hello": "World"}

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

@app.get("/addItem")
def addItem(
        user_id: Union[str, None] = None,
        name: Union[str, None] = None,
        expiry_date: Union[datetime, None] = None,
        ):
    if user_id== None:
        return {"Error": "user_id is invalid"}
    if name == None:
        return {"Error": "name is invalid"}
    if expiry_date == None:
        return {"Error": "expiry_date is invalid"}
    if not db.users.find_one({
        "_id": ObjectId(user_id)
        }):
        return {"Error": "user_id is invalid"}
    item = db.items.insert_one({
        "user_id": user_id,
        "name": name,
        "expiry_date": expiry_date,
        })
    return {"item_id": str(item.inserted_id)}

@app.get("/listItems")
def listItems(
        ):
    t = datetime.now()
    return [{"name":i["name"],"expiry_date":str(i["expiry_date"]-t)} for i in db.items.find({})]
