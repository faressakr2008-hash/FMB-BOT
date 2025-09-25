import os
import io
from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image

# جلب التوكن من الـ Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# فولدر الخلفيات
BG_FOLDER = "backgrounds"

def handle_photo(update, context):
    # تحميل الصورة من تليجرام
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file_bytes = io.BytesIO()
    file.download(out=file_bytes)

    # فتح الصورة
    file_bytes.seek(0)
    user_img = Image.open(file_bytes).convert("RGBA")

    # اختيار الخلفية بناءً على النص
    text = (update.message.caption or "").strip().lower()
    if text == "اخبار":
        bg_path = os.path.join(BG_FOLDER, "news.png")
    elif text == "تحليل":
        bg_path = os.path.join(BG_FOLDER, "analysis.png")
    elif text == "احصائيات":
        bg_path = os.path.join(BG_FOLDER, "stats.png")
    else:
        update.message.reply_text("من فضلك اكتب (اخبار / تحليل / احصائيات) مع الصورة.")
        return

    # فتح الخلفية
    bg_img = Image.open(bg_path).convert("RGBA")

    # تغيير حجم صورة المستخدم لتناسب الخلفية
    user_img = user_img.resize((bg_img.width, bg_img.height))

    # تركيب الصورة على الخلفية
    combined = Image.alpha_composite(bg_img, user_img)

    # تجهيز الصورة للرد
    output_bytes = io.BytesIO()
    combined.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    update.message.reply_photo(photo=output_bytes)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
