from glob import glob
from random import choice
import os
from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from utils import (play_random_numbers, main_keyboard,
                   has_object_on_img)


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    print('Вызван start')
    update.message.reply_text(
        f"Здравствуй, чувачок {user['emoji']}",
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(
        f'{text} {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def guess_num(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    print(context.args)
    if context.args:
        try:
            user_num = int(context.args[0])
            message = play_random_numbers(user_num)
        except (ValueError, TypeError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_peace_img(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    peace_img_list = glob('images/peace*.jp*g')
    peace_img_filename = choice(peace_img_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, photo=open(peace_img_filename, 'rb'),
        reply_markup=main_keyboard()
        )


def send_dog_img(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    dog_img_list = glob('images/dog*.jp*g')
    dog_img_filename = choice(dog_img_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, photo=open(dog_img_filename, 'rb'),
        reply_markup=main_keyboard()
        )


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f'Твои координаты, бро {coords} {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    update.message.reply_text('Изучаю фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads',
                             f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Сохранил фото! Спасибо, бро!')
    if has_object_on_img(file_name, 'dog'):
        update.message.reply_text('Обнаружен пёсик, сохраняю себе')
        new_file_name = os.path.join('images', f'dog{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Соррян, бро! Тут нет пёсика')


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Йо, братанчик, ты подписался! Благодарочка!')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Разочаровал ты меня, конечно... Отписан...')