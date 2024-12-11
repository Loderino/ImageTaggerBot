from enum import Enum, auto, unique

from image_tagger_bot.modes.generation import GENERATION_CMD
from image_tagger_bot.modes.markup import MARKUP_CMD

@unique
class BotStates(Enum):
    """Contains the modes of operation of the bot"""

    GENERATION = auto()
    MARKUP = auto()


CMD_TO_STATE = {
    BotStates.GENERATION: GENERATION_CMD,
    BotStates.MARKUP: MARKUP_CMD,
}