from emoji import emojize
import logging
import settings
from glob import glob
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, чувачок {context.user_data['emoji']}")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}')

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
    update.message.reply_text(message)

def send_peace_img(update, context):
    peace_img_list = glob('images/peace*.jp*g')
    peace_img_filename = choice(peace_img_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(peace_img_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_num))
    dp.add_handler(CommandHandler("peace", send_peace_img))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()

