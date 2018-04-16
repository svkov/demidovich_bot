import logging

from telegram.ext import Updater, CommandHandler

token = '564309290:AAEc7cVxKJanPjua_RfhRPGopxzyo8b3V74'

logger = None
last_task = None


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
    page = str(page)
    if len(page) == 1:
        page = '00' + page
    elif len(page) == 2:
        page = '0' + page
    elif len(page) >= 4:
        page = page[:2]
    return open('res/pages/demidovich_for_highschool-' + page + '.jpg', 'rb')


def start(bot, update):
    update.message.reply_text('Привет! Введи /get_task и номер задания, чтобы начать решать')


def get_task(bot, update):
    text = update.message['text'].split()
    if len(text) == 1:
        update.message.reply_text('Ты забыл ввести номер задания!')
    else:
        page = get_page_number(text[1])
        pic = get_picture(page)
        bot.send_photo(update.message.chat_id, pic)


def get_page(bot, update):
    text = update.message['text'].split()
    if len(text) == 1:
        update.message.reply_text('Ты забыл ввести номер страницы!')
    else:
        pic = get_picture(int(text[1]))
        bot.send_photo(update.message.chat_id, pic)


def error(bot, update, error):
    if logger:
        logger.warning('Update "%s" caused error "%s"', update, error)


def answer(bot, update):
    if last_task:
        pic = get_picture(last_task)
        bot.send_photo(update.message.chat_id, pic)


def main():
    global logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    updater = Updater(token)

    dp = updater.dispatcher

    print('Bot starts to work')

    start_handler = CommandHandler('start', start)
    get_task_handler = CommandHandler('get_task', get_task)
    get_page_handler = CommandHandler('get_page', get_page)
    get_answer_handler = CommandHandler('answer', answer)

    dp.add_handler(get_answer_handler)
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

    main()
