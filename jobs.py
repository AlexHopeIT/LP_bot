from datetime import datetime
from db import db, get_subscribed
from telegram.error import BadRequest


def send_updates(context):
    text = "Сейчас " + datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(text)
    for user in get_subscribed(db):
        print(user['chat_id'])
        try:
            context.bot.send_message(chat_id=user['chat_id'], text=text)
            print('it`s ok')
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден")
