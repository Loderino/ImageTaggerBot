import os
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from image_tagger.tagger import Tagger
from constants import IMAGE_TAGGER_MODEL_PATH, IMAGE_TAGGER_TOKENIZER_PATH

class PhotoHandler:
    def __init__(self):
        self.abs_prefix = Path("./images/").absolute()
        self.tagger = Tagger()
        self.tagger.model_path = IMAGE_TAGGER_MODEL_PATH
        self.tagger.tokenizer_path = IMAGE_TAGGER_TOKENIZER_PATH
        self.tagger.load_model()
        if not self.abs_prefix.exists():
            Path.mkdir(self.abs_prefix)
        try:
            self.image_number = max(map(lambda x: int(x.split(".")[0]), filter(lambda x: x.endswith("jpg"), os.listdir(self.abs_prefix))))
            print(self.image_number)
        except ValueError:
            self.image_number = 0

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:        
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_extension = os.path.splitext(file.file_path)[1]
        self.image_number += 1
        file_name = f"{self.image_number}{file_extension}"
        file_path = self.abs_prefix/file_name
        
        await file.download_to_drive(file_path)
        tags = self.tagger.generate_desc(file_path)
        await update.message.reply_text(', '.join(tags))