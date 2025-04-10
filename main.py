from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
import yt_dlp
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! YouTube havolasini yuboring, men sizga video faylni qaytaraman.")

async def download_video_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❌ Noto‘g‘ri URL. Iltimos, YouTube havolasini yuboring.")
        return

    await update.message.reply_text('⏳ Yuklab olinmoqda...')

    with tempfile.TemporaryDirectory() as temp_dir:
        video_opts = {
            'format': 'bv+ba/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
        }


        try:
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = ydl.prepare_filename(info)

            # Fayl hajmini tekshirish
            if os.path.getsize(video_path) > 49 * 1024 * 1024:
                await update.message.reply_text("⚠️ Video fayli 50MB dan katta, Telegram orqali yuborib bo‘lmaydi.")
                return

            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file)

        except Exception as e:
            logging.exception("Xatolik yuz berdi")
            await update.message.reply_text(f"❌ Xatolik yuz berdi:\n{str(e)}")

def main():
    application = ApplicationBuilder().token("7900585023:AAHP4UmJnDo3_vEoN2i9mN-86nvkm281vvs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video_audio))

    application.run_polling()

if __name__ == '__main__':
    main()
