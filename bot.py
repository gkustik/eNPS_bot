import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup

from eNPS import eNPS_start, eNPS_rating, eNPS_comment, eNPS_comment_skip, eNPS_dontknow, main_keyboard
from db import db, get_user
import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)


def greet_user(update, context):
    user = get_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f"Здравствуй, user_name!\nПоследний процесс ревью проходил date_last_review.\nПоследний eNPS = last_eNPS_score был собран date_last_eNPS",
        reply_markup = main_keyboard()
    )

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher

    eNPS = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Замерить eNPS)$'), eNPS_start)
        ],
        states={
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10)$'), eNPS_rating)],
            "comment": [
                CommandHandler("skip", eNPS_comment_skip),
                MessageHandler(Filters.text, eNPS_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, eNPS_dontknow)
        ]
    )
    dp.add_handler(eNPS)
    dp.add_handler(CommandHandler("start", greet_user))
   

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()