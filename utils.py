from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile)
    return user_data['emoji']

def play_random_numbers(user_num):
    bot_num = randint(user_num - 10, user_num + 10)
    if user_num > bot_num:
        message = f'Кожаный, ты выбрал число {user_num}, а моё число: {bot_num}! Твоя взяла!'
    elif user_num == bot_num:
        message = f'Число юзера: {user_num}, число бота: {bot_num}. Ничья!'
    else:
        message = f'Свершилось, кожаный! Ты выбрал число {user_num}, а я выбрал {bot_num}! Я победил! Уга-га-га!'
    return message

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Отправь peace', KeyboardButton('Моя геолокация', request_location=True)]
            ]
            )