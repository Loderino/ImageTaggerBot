from telegram import BotCommand
from telegram.ext import filters

GENERATION_CMD = [
    BotCommand("/help", "получить справку"),
    BotCommand("/markup_mode", "перейти в режим разметки фото"),
]

ALLOWED_INPUT_FILE_FILTERS = (
    filters.PHOTO
)
