
import pymongo, os

DB_URI = "mongodb+srv://adityajsru17:aditya310708@aditya.c2ebyse.mongodb.net/?retryWrites=true&w=majority&appName=Aditya"
DB_NAME = "filesharexbot"

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    total = user_data.count_documents({})
    return bool(found), total

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return