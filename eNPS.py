from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from db import get_user, save_eNPS


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Замерить eNPS']
    ])

def eNPS_start(update, context):
    reply_keyboard = [["1", "2", "3", "4", "5","6", "7", "8", "9", "10"]]
    update.message.reply_text(
     "Оцените, насколько вы готовы рекомендовать ST, как место работы?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "rating"

def eNPS_rating(update, context):
    context.user_data['eNPS']['rating'] = int(update.message.text)
    update.message.reply_text("Напишите комментарий, или нажмите /skip чтобы пропустить")
    return "comment"


def eNPS_comment(update, context):
    context.user_data['eNPS']['comment'] = update.message.text
    user = get_user(db, update.effective_user, update.message.chat.id)
    save_eNPS(db, user['user_id'], context.user_data['eNPS'])
    update.message.reply_text("Спасибо, ваша оценка и комментарий записаны. Оценка eNPS прийдет как только соберем ответы со всех.")
    return ConversationHandler.END


def eNPS_comment_skip(update, context):
    user = get_user(db, update.effective_user, update.message.chat.id)
    save_eNPS(db, user['user_id'], context.user_data['eNPS'])
    update.message.reply_text("Спасибо, ваша оценка и комментарий записаны. Оценка eNPS прийдет как только соберем ответы со всех.")
    return ConversationHandler.END


def eNPS_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")
    

