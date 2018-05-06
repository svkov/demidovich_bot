import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

token = '564309290:AAEc7cVxKJanPjua_RfhRPGopxzyo8b3V74'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
last_task = None
last_page = 1
CHOOSING, CHOOSE_TASK, CHOOSE_PAGE = range(3)

pages_keyboard = [[InlineKeyboardButton('<<<', callback_data='left'),
                   InlineKeyboardButton('>>>', callback_data='right')],
                  [InlineKeyboardButton('Ответы', callback_data='answer')],
                  [InlineKeyboardButton('Новое задание', callback_data='task')],
                  [InlineKeyboardButton('Новая страница', callback_data='page')]]
pages_markup = InlineKeyboardMarkup(pages_keyboard)

start_keyboard = [[InlineKeyboardButton('Задание', callback_data='1'),
                 InlineKeyboardButton('Страница', callback_data='2')]]
start_markup = InlineKeyboardMarkup(start_keyboard)

def get_data_from_smth():
    with open('res/numbers/smth.txt', 'r') as db:
        all_tasks = list(map(lambda x: x.split(), db.read().split('\n')))
        all_tasks.pop()
        all_tasks = list(map(lambda x: (int(x[0]), x[1]), all_tasks))
        # all_tasks = list(map(lambda x: print(x), all_tasks))

        all_tasks.sort(key=lambda x: x[0])
        all_tasks = all_tasks[5:]
    return all_tasks


def get_data():
    with open('res/numbers/sorted.txt') as inp:
        r = inp.read()
        r = r.split('\n')
        r = list(map(lambda x: x.split(), r))
    return r


def get_page_number(task):
    global last_task
    task = int(task)
    last_task = task
    for i in range(len(data) - 1):
        try:
            if int(data[i][1]) > task:
                return int(data[i - 1][0])
        except:
            pass
    return 1


def get_picture(page):
    page = str(int(page) - 2)
    if len(page) == 1:
        page = '00' + page
    elif len(page) == 2:
        page = '0' + page
    elif len(page) >= 4:
        page = page[:2]
    return open('res/pages/demidovich_for_highschool-' + page + '.jpg', 'rb')


def start(bot, update):
    update.message.reply_text('Привет! Выбери, что тебе нужно!', reply_markup=start_markup)


def get_task(bot, update):
    global last_page, last_task
    text = update.message['text'].split()
    if len(text) > 1:
        update.message.reply_text('Ты ввел что-то странное')
    else:
        page = get_page_number(text[0])
        last_task = int(text[0])
        last_page = page
        pic = get_picture(page)
        bot.send_photo(update.message.chat_id, pic, reply_markup=pages_markup)


def get_page(bot, update):
    global last_page, last_task
    text = update.message['text'].split()
    if len(text) > 1:
        update.message.reply_text('Ты ввел что-то странное')
    else:
        last_page = int(text[0])
        pic = get_picture(int(text[0]))
        bot.send_photo(update.message.chat_id, pic, reply_markup=pages_markup)


def error(bot, update, error):
    if logger:
        logger.warning('Update "%s" caused error "%s"', update, error)


def answer(bot, update):
    if last_task:
        pic = get_picture(last_task)
        bot.send_photo(update.message.chat_id, pic)


def button(bot, update):
    global last_page
    query = update.callback_query
    data = query.data
    print(data)

    if data == '1':
        bot.edit_message_text(text='Введи номер задания', chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return CHOOSE_TASK
    elif data == '2':
        bot.edit_message_text(text='Введи номер страницы', chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return CHOOSE_PAGE
    elif data == 'task':
        bot.send_message(text='Введи номер задания', chat_id=query.message.chat_id)
        return CHOOSE_TASK
    elif data == 'page':
        bot.send_message(text='Введи номер страницы', chat_id=query.message.chat_id)
        return CHOOSE_PAGE
    elif data == 'left':
        if last_page > 1:
            last_page -= 1
        bot.send_photo(query.message.chat_id, get_picture(last_page), reply_markup=pages_markup)
    elif data == 'right':
        if last_page < 625:
            last_page += 1
        bot.send_photo(query.message.chat_id, get_picture(last_page), reply_markup=pages_markup)
    elif data == 'answer':
        bot.send_photo(query.message.chat_id, get_picture(478), reply_markup=pages_markup)


def main():
    global updater

    dp = updater.dispatcher

    print('Bot starts to work')

    start_handler = CommandHandler('start', start)
    # get_task_handler = CommandHandler('get_task', get_task)
    # get_page_handler = CommandHandler('get_page', get_page)
    get_task_handler = MessageHandler(Filters.text, get_task)
    get_page_handler = MessageHandler(Filters.text, get_page)
    get_answer_handler = CommandHandler('answer', answer)
    choosing_handler = CallbackQueryHandler(button)
    # exit_handler = CommandHandler('exit')

    handler = ConversationHandler(
        entry_points=[start_handler],

        states={
            # CHOOSING: [choosing_handler],
            CHOOSE_TASK: [get_task_handler],
            CHOOSE_PAGE: [get_page_handler]
        },
        fallbacks=[]
    )

    dp.add_handler(choosing_handler)
    dp.add_handler(get_answer_handler)
    dp.add_handler(handler)
    dp.add_handler(get_page_handler)
    dp.add_handler(start_handler)
    dp.add_handler(get_task_handler)
    dp.add_error_handler(error)

    updater.start_polling()


if __name__ == '__main__':
    data = get_data()
    data.pop()
    # print(data)
    # print(get_page_number(500))
    updater = Updater(token)
    main()
