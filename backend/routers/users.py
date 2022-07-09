from fastapi import APIRouter
from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
from pymongo import MongoClient

client = MongoClient("127.0.0.1:27017")
db = client.lifehack

router = APIRouter(
        prefix="/users",
        tags=["users"]
        )

@router.post("/createUser")
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

@router.post("/login")
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

@router.get("/getUserById")
def getUserById(id: Union[str, None] = None):
    usr = db.users.find_one(
    {
        "_id" : ObjectId(id)
    }
    )
    if usr:
        return {"username": usr["username"], "location": usr["location"]}
    else:
        return {"Error": "Problem retrieving user"}

@router.put("/updateUser")
def updateUser(
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        location: Union[str, None] = None,
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
        if location:
            updated = db.users.update_one({"_id": ObjectId(id)}, 
            {"$set":
                {"location": location} 
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
    

