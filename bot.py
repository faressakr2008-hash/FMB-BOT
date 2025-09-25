
import os
from telegram.ext import Updater, MessageHandler, Filters
from rembg import remove
from PIL import Image
import io

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def handle_photo(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file_bytes = io.BytesIO()
    file.download(out=file_bytes)
    
    input_image = Image.open(file_bytes)
    output_image = remove(input_image)
    
    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    
    update.message.reply_photo(photo=output_bytes)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
updater.start_polling()
