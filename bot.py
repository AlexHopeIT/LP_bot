import logging
from handlers import (greet_user, talk_to_me, guess_num, 
                      user_coordinates, send_peace_img, send_dog_img, check_user_photo)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_num))
    dp.add_handler(CommandHandler("peace", send_peace_img))
    dp.add_handler(CommandHandler("dog", send_dog_img))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.regex('^(Отправь peace)$'), send_peace_img))
    dp.add_handler(MessageHandler(Filters.regex('^(Отправь пёсика)$'), send_dog_img))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()

