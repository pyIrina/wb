from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON_YOKOSUN = 'YOKOSUN'
BUTTON_JOONIES = 'JOONIES'

BUTTON_M = 'M'
BUTTON_L = 'L'
BUTTON_XL = 'XL'


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON_YOKOSUN),
            KeyboardButton(BUTTON_JOONIES),
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_base_form_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON_M),
            KeyboardButton(BUTTON_L),
            KeyboardButton(BUTTON_XL),
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
