from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
import yt_dlp
import os
import re

DOWNLOADS_DIR = 'downloads'  # Yuklamalar uchun papka

# Yuklamalar uchun papkani yaratish
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def sanitize_filename(filename):
    # Fayl nomidagi noaniq belgilarni olib tashlash
    return re.sub(r'[\\/*?:"<>|]', "", filename)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! Men video va audio yuklovchi botman. Linkni yuboring.')

async def download_video_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('Video va audio yuklanmoqda...')

    video_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOADS_DIR, sanitize_filename('%(title)s.%(ext)s')),
    }

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOADS_DIR, sanitize_filename('%(title)s.%(ext)s')),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/usr/bin/ffmpeg',  # ffmpeg joylashgan yo'l
    }

    video_filename = None
    audio_filename = None

    try:
        # Videoni yuklab olish
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(video_info)

        # Audioni yuklab olish
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            audio_info = ydl.extract_info(url, download=True)
            audio_filename = os.path.join(DOWNLOADS_DIR, f"{sanitize_filename(audio_info['title'])}.mp3")

        # Fayllarni yuborish
        await update.message.reply_video(video=open(video_filename, 'rb'))
        await update.message.reply_audio(audio=open(audio_filename, 'rb'))

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {str(e)}")

    finally:
        # Fayllarni o'chirish
        if video_filename and os.path.exists(video_filename):
            os.remove(video_filename)
        if audio_filename and os.path.exists(audio_filename):
            os.remove(audio_filename)


def main():
    application = ApplicationBuilder().token("7900585023:AAHKTO0RqRtjWacyYgZZaitKnR8doTBge-o").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video_audio))

    application.run_polling()

if __name__ == '__main__':
    main()
