import logging
from handlers import (greet_user, talk_to_me, guess_num,
                      user_coordinates, send_peace_img, send_dog_img,
                      check_user_photo, subscribe, unsubscribe)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from anketa import (anketa_start, anketa_name,
                    anketa_rating, anketa_skip,
                    anketa_comment, anketa_dontknow)
from jobs import send_updates
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    jq = mybot.job_queue
    jq.run_repeating(send_updates, interval=10, first=1)

    dp = mybot.dispatcher

    anketa = ConversationHandler(
       entry_points=[
           MessageHandler(Filters.regex('^(Заполнить анкету-отзыв о боте)$'),
                          anketa_start)
       ],
       states={
        "name": [MessageHandler(Filters.text, anketa_name)],
        "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'),
                                  anketa_rating)],
        "comment": [CommandHandler('skip', anketa_skip),
                    MessageHandler(Filters.text, anketa_comment)]
        },
       fallbacks=[
           MessageHandler(Filters.text | Filters.animation | Filters.photo |
                          Filters.location | Filters.document, anketa_dontknow)
       ]
    )

    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_num))
    dp.add_handler(CommandHandler("peace", send_peace_img))
    dp.add_handler(CommandHandler("dog", send_dog_img))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.regex('^(Отправь peace)$'),
                                  send_peace_img))
    dp.add_handler(MessageHandler(Filters.regex('^(Отправь пёсика)$'),
                                  send_dog_img))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
