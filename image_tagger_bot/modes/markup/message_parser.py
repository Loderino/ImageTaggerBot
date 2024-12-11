from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

from image_tagger_bot.modes.markup.marker import Marker


class MarkupMessageHandler:
    def __init__(self):
        self.marker = Marker()
    
    async def send_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        image_number = await self.marker.get_random_non_marked_image()
        if image_number is None:
            await context.bot.send_message(update.effective_chat.id, "Похоже, неразмеченные картинки закончились. Можешь в режиме генерации тегов прислать мне новые!")
            return
        context.user_data["number"] = image_number
        print(image_number)
        image_path = Path(f"./images/{image_number}.jpg")
        try:
            # Открываем файл и отправляем его
            with open(image_path, 'rb') as photo_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo_file
                )
            
            print(f"Фото успешно отправлено: {image_path}")
        
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            await context.bot.send_message(update.effective_chat.id, text="Фото застряло... Воспользуйся командой /retry.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        delimiter = ", " if text.find(",") > -1 else " "
        tags = text.split(delimiter)
        self.marker.new_description(context.user_data["number"], tags)
        await self.send_photo(update, context)
        

    