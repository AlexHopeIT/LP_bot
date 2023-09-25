from glob import glob
from random import choice
import os
from utils import get_smile, play_random_numbers, main_keyboard, has_object_on_img

def greet_user(update, context):
    print('Вызван start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, чувачок {context.user_data['emoji']}",
        reply_markup=main_keyboard()
        )
    
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(
        f'{text} {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
        )
    
def guess_num(update, context):
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
    peace_img_list = glob('images/peace*.jp*g')
    peace_img_filename = choice(peace_img_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, photo=open(peace_img_filename, 'rb'), 
        reply_markup=main_keyboard()
        )
    

def send_dog_img(update, context):
    dog_img_list = glob('images/dog*.jp*g')
    dog_img_filename = choice(dog_img_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, photo=open(dog_img_filename, 'rb'), 
        reply_markup=main_keyboard()
        )


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f'Твои координаты, бро {coords} {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    update.message.reply_text('Изучаю фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Сохранил фото! Спасибо, бро!')
    if has_object_on_img(file_name, 'dog'):
        update.message.reply_text('Обнаружен пёсик, сохраняю в свою библиотеку')
        new_file_name = os.path.join('images', f'dog{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Соррян, бро! Тут нет пёсика')
