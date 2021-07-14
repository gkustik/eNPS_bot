from datetime import datetime
from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]

def get_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id
        }
        db.users.insert_one(user) #return ("Вас нет в ST")
    return user


def save_eNPS(db, user_id, eNPS_data):
    user = db.users.find_one({"user_id": user_id})
    eNPS_data['created'] = datetime.now()
    if 'eNPS' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'eNPS': [eNPS_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'eNPS': eNPS_data}}
        )

