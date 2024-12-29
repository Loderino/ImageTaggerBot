from telegram import BotCommand
from telegram.ext import filters

MARKUP_CMD = [
    BotCommand("/help", "получить справку"),
    BotCommand("/retry", "вызвать картинку"),
    BotCommand("/top", "получить топ пользователей, разметивших больше всего картинок"),
    BotCommand("/generation_mode", "перейти в режим генерации тегов"),
]

ALLOWED_INPUT_FILE_FILTERS = (
    filters.PHOTO
)
