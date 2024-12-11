import aiofiles
import pickle

from image_tagger_bot import CMD_TO_STATE, BotStates

async def read_pickle_data(filepath: str):
    """
    Asynchronously read data from a pickle file.

    Args:
        filepath (str): The path to the pickle file.

    Returns:
        Any | None: The data read from the pickle file, or None if the file does not exist or cannot be read.
    """
    try:
        async with aiofiles.open(filepath, "rb") as file:
            return pickle.loads(await file.read())
    except (pickle.PickleError, EOFError, FileNotFoundError):
        return None
    

from telegram import BotCommandScopeChat
from telegram.ext import ContextTypes, ConversationHandler


async def change_user_state(
    conv_handler: ConversationHandler, context: ContextTypes.DEFAULT_TYPE, user_id: int, new_state: BotStates
) -> None:
    """
    Changes the state of the user in the conversation handler.

    Args:
        conv_handler (ConversationHandler): The conversation handler.
        context (ContextTypes.DEFAULT_TYPE): The Telegram context object.
        user_id (int): The Telegram ID of the user.
        new_state (BotStates): The new state of the user.
    """
    await context.bot.set_my_commands(CMD_TO_STATE[new_state], scope=BotCommandScopeChat(chat_id=user_id))
    # pylint: disable=protected-access
    conv_handler._update_state(new_state, (user_id, user_id))
