from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

from constants import TOP_PATH
from image_tagger_bot.json_files_handler import read_json_file, update_json_file
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
        context.user_data["marked_pictures"] = context.user_data.get("marked_pictures", 0) + 1
        update_json_file(TOP_PATH, {str(update.effective_chat.id): context.user_data["marked_pictures"]})
        self.marker.new_description(context.user_data["number"], tags)
        await self.send_photo(update, context)

    async def send_top_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        data = read_json_file(TOP_PATH)
        if data:
            top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
            #TODO добавить логику для пользователей без юзернеймов
            top_str = ""
            for i, (tg_id, marked_pictures) in enumerate(top):
                user_chat = await context.bot.getChat(int(tg_id))
                username = user_chat.username if user_chat.username else user_chat.first_name
                top_str += f"{i+1}) {username}: {marked_pictures}\n"
            await context.bot.send_message(update.effective_chat.id, top_str)
        else:
            await context.bot.send_message(update.effective_chat.id, "Ещё никто не размечал картинки =(")