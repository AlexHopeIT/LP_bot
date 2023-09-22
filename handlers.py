from glob import glob
from random import choice
from utils import get_smile, play_random_numbers, main_keyboard

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

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f'Твои координаты, бро {coords} {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
    )

