#(©)CodeXBotz

async def check_verification(user_id):
    # Implement this to check verification status from your database
    # Example MongoDB implementation:
    user = await users_collection.find_one({'_id': user_id})
    if user:
        return {
            'is_verified': user.get('is_verified', False),
            'verified_time': user.get('verified_time'),
            'verify_token': user.get('verify_token')
        }
    return {'is_verified': False, 'verified_time': None, 'verify_token': None}

async def update_verification(user_id, is_verified=None, verified_time=None, token=None):
    # Implement this to update verification status in your database
    # Example MongoDB implementation:
    update_data = {}
    if is_verified is not None:
        update_data['is_verified'] = is_verified
    if verified_time is not None:
        update_data['verified_time'] = verified_time
    if token is not None:
        update_data['verify_token'] = token
    
    await users_collection.update_one(
        {'_id': user_id},
        {'$set': update_data},
        upsert=True
    )


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
