#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

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


# Chat Group Data

group_data = database['groups']


async def present_group(chat_id: int):
    found = group_data.find_one({'_id': chat_id})
    total = group_data.count_documents({})
    return bool(found), total

async def add_group(chat_id: int):
    group_data.insert_one({'_id': chat_id})
    return

async def del_group(chat_id: int):
    group_data.delete_one({'_id': chat_id})
    return

async def full_groupbase():
    group_docs = group_data.find()
    group_ids = []
    for doc in group_docs:
        group_ids.append(doc['_id'])
        
    return group_ids


# Disable Quizzez Data

disable_quizzez_data = database['disable_quizzez']


async def unpresent_quizzez(chat_id: int):
    found = disable_quizzez_data.find_one({'_id': chat_id})
    return bool(found)

async def add_quizzez(chat_id: int):
    disable_quizzez_data.insert_one({'_id': chat_id})
    return

async def del_quizzez(chat_id: int):
    disable_quizzez_data.delete_one({'_id': chat_id})
    return

async def full_quizzezbase():
    disable_quizzez_docs = disable_quizzez_data.find()
    disable_quizzez_ids = []
    for doc in disable_quizzez_docs:
        disable_quizzez_ids.append(doc['_id'])
        
    return disable_quizzez_ids
