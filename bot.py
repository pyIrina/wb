import csv
import os
import json
from main import Client
from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from buttons import get_base_reply_keyboard
from buttons import get_base_form_keyboard
from buttons import BUTTON_YOKOSUN
from buttons import BUTTON_JOONIES
from buttons import BUTTON_M
from buttons import BUTTON_L
from buttons import BUTTON_XL

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BUTTON_START = '/start'
SIZE = {
    'M': 'f566=70394',
    'L': 'f566=70398',
    'XL': 'f566=79423',
}

BRANDS = {
    'YOKOSUN': '?brand=22688&',
    'JOONIES': '?brand=51526&'

}


def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Привет! Выберите марку",
        reply_markup=get_base_reply_keyboard(),
    )


def processing_csv(update: Update, context: CallbackContext):
    with open('test.csv', newline='', encoding='utf-8') as File:
        reader = csv.DictReader(File)
        row_count = sum(1 for row in reader if row)
        update.message.reply_text(
            text=f'Всего найдено: {row_count} варианта(ов)\n\n')
        File.seek(0)
        next(reader, None)
        for row in reader:
            if row:
                update.message.reply_text(
                    text=f'''Цена со скидкой - {row['Скидка']}₽. \n {row['Ссылка']}''')
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text="Поиск завершен!\n\nНажмите /start чтобы начать заново",
        reply_markup=ReplyKeyboardRemove(),
    )


def do_size(update: Update, context: CallbackContext):
    text = update.message.text
    with open('selected_brend.json', 'r', encoding='utf-8') as file:
        brand_json = json.load(file)

    parser = Client()
    parser.run(BRANDS[brand_json], SIZE[text])
    processing_csv(update=update, context=context)


def do_yokosun(update: Update):
    update.message.reply_text(
        text="Выберите размер\n\n",
        reply_markup=get_base_form_keyboard(),
    )


def do_joonies(update: Update):
    update.message.reply_text(
        text="Выберите размер\n\n",
        reply_markup=get_base_form_keyboard(),
    )


def save_brand_file(text):
    with open('selected_brend.json', 'w', encoding='utf-8') as file:
        json.dump(text, file, ensure_ascii=False, sort_keys=True, indent=4)


def do_echo(update: Update, context: CallbackContext):
    text = update.message.text
    if text == BUTTON_YOKOSUN:
        save_brand_file(text)
        return do_yokosun(update=update)
    elif text == BUTTON_JOONIES:
        save_brand_file(text)
        return do_joonies(update=update)
    elif text == BUTTON_M or text == BUTTON_L or text == BUTTON_XL:
        return do_size(update=update, context=context)

    else:
        reply_text = "Команда не распознана, попробуйте еще раз!"
        update.message.reply_text(
            text=reply_text,
        )


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def main():
    REQUEST_KWARGS = {
        'proxy_url': 'socks5://184.185.2.146:47659',
        'urllib3_proxy_kwargs': {
            'assert_hostname': 'False',
            'cert_reqs': 'CERT_NONE'
            # 'username': 'user',
            # 'password': 'password'
        }
    }

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", do_start)
    dispatcher.add_handler(start_handler)
    message_handler = MessageHandler(Filters.text, do_echo)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
