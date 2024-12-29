from telegram import BotCommandScopeChat, Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters
)

from image_tagger_bot import BotStates, CMD_TO_STATE
from image_tagger_bot.json_files_handler import read_json_file
from image_tagger_bot.modes.generation.photo_handler import PhotoHandler
from image_tagger_bot.utils.common_functions import read_pickle_data
from image_tagger_bot.modes.markup.message_parser import MarkupMessageHandler
from constants import BOT_TOKEN, CONV_NAME, PERSISTENCE_PATH, TOP_PATH

class TGBot:
    def __init__(self) -> None:
        self.bot = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .concurrent_updates(True)
            .http_version("1.1")
            .get_updates_http_version("1.1")
            .persistence(PicklePersistence(filepath=PERSISTENCE_PATH))
            .post_init(self.initialize_bot)
            .build()
        )
        self.conv_handler = None
        self.photo_handler = PhotoHandler()
        self.message_handler = MarkupMessageHandler()
        self.add_handlers()
        

    def add_handlers(self) -> None:
        """
        Add handlers to the bot.

        Each handler is a function that takes an update and a context and returns `BotStates` or None.
        If the function returns `BotStates`, the bot will change the current state to that state.
        If the function returns None, the bot will not change the current state.
        All states are defined in the `BotStates` enum and saved in the `persistence` file.
        """
        self.conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.start_command)
            ],
            states=self.get_states(),
            fallbacks=[
                MessageHandler(filters.ALL, self.unknown),
            ],
            name = CONV_NAME,
            persistent=True,
        )
        self.bot.add_handler(self.conv_handler)
   


    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Method for handling unknown events.

        Args:
            update (Update): The update object containing information about the user.
            context (ContextTypes.DEFAULT_TYPE): The Telegram context object.
        """
        await update.message.reply_text("Не понимаю. Пожалуйста, отправьте фото.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Method for handling /help command.

        Args:
            update (Update): The update object containing information about the user.
            context (ContextTypes.DEFAULT_TYPE): The Telegram context object.
        """
        await update.message.reply_text('Для генерации тегов из изображений просто отправь мне фото. Все загруженные фотографии попадут в обучающую выборку для моего дальнейшего обучения.')

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Entry point for the bot user.

        Args:
            update (Update): The update object containing information about the user.
            context (ContextTypes.DEFAULT_TYPE): The Telegram context object.

        Returns:
            int: id of generation bot state.
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который может извлекать признаки из изображений и отдавать теги для них. Используй /help для получения справки.")
        return BotStates.GENERATION
    
    def get_states(self) -> dict[BotStates, list]:
        """
        Get states for the bot.

        Returns:
            Dict[BotStates, List]: The dictionary containing bot states and corresponding handlers.
        """
        states = {
            BotStates.GENERATION:[
                CommandHandler("help", self.help_command),
                CommandHandler("markup_mode", self.markup_mode),
                MessageHandler(filters.PHOTO, self.photo_handler.handle_photo)
            ],
            BotStates.MARKUP:[
                CommandHandler("help", self.help_command),
                CommandHandler("retry", self.message_handler.send_photo),
                CommandHandler("top", self.message_handler.send_top_message),
                CommandHandler("generation_mode", self.generation_mode),
                MessageHandler(filters.TEXT, self.message_handler.handle_message),
            ]
        }
        return states

    async def generation_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.set_my_commands(
            CMD_TO_STATE[BotStates.GENERATION], scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
        )
        await context.bot.send_message(update.effective_chat.id, "Вы перешли в режим генерации тегов.")
        return BotStates.GENERATION
    
    async def markup_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["marked_pictures"] = read_json_file(TOP_PATH).get(update.effective_chat.id, 0)
        await context.bot.set_my_commands(
            CMD_TO_STATE[BotStates.MARKUP], scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
        )
        await context.bot.send_message(update.effective_chat.id, "Вы перешли в режим разметки картинок. Пишите теги через пробел.")
        await self.message_handler.send_photo(update, context)
        return BotStates.MARKUP

    async def initialize_bot_commands(self, application: Application) -> None:
        """
        Initializing the bot's commands.

        Users receive a set of commands according to their state. The state is set in the `persistence` file.

        Args:
            application (Application): The Telegram application object.
        """
        if data := await read_pickle_data(PERSISTENCE_PATH):
            conversations = data.get("conversations", {}).get(CONV_NAME, {})
            for uid, state in conversations.items():
                try:
                    await application.bot.set_my_commands(
                        CMD_TO_STATE[state], scope=BotCommandScopeChat(chat_id=uid[0])
                    )
                except TelegramError as e:
                    pass
                    # logger.error(e, exc_info=True)

    def run_polling(self) -> None:
        """
        Starting the bot's polling cycle.

        Before the bot starts polling, it starts a background task to clear the context of inactive users.
        """
        self.bot.run_polling(allowed_updates=Update.ALL_TYPES)

    async def initialize_bot(self, application: Application) -> None:
        """
        Executed at bot startup:
        - initialise command sets depending on state,

        Args:
            application (Application): The Telegram application object.
        """
        await self.initialize_bot_commands(application)