from emoji import emojize
from datetime import datetime
from random import choice
from pymongo import MongoClient

from settings import MONGO_LINK, MONGO_DB, USER_EMOJI


client = MongoClient(MONGO_LINK)

db = client[MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id,
            'emoji': emojize(choice(USER_EMOJI))
        }
        db.users.insert_one(user)
    return user


def save_anketa(db, user_id, anketa_data):
    user = db.users.find_one({'user_id': user_id})
    anketa_data['created'] = datetime.now()
    if 'anketa' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'anketa': [anketa_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'anketa': [anketa_data]}}
        )


def subscribe_user(db, user_data):
    if not user_data.get('subcribed'):
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subcribed': True}}
        )


def unsubscribe_user(db, user_data):
    db.users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'subcribed': False}}
    )


def get_subscribed(db):
    return db.users.find({'subscribed': True})
