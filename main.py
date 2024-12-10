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
    await update.message.reply_text('Salom! Linkni yuboring, men video yoki audio chiqarib olaman.')

async def download_video_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('Video va audio yuklanmoqda...')

    video_opts = {
        'format': 'best',  # Eng yaxshi video format
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),  # To'g'ri yo'lni ajratish
    }

    audio_opts = {
        'format': 'bestaudio/best',  # Eng yaxshi audio format
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Audio chiqarib olish
            'preferredcodec': 'mp3',     # MP3 formatga aylantirish
            'preferredquality': '192',   # Sifat darajasi
        }],
        'ffmpeg_location': 'C:/Users/user/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-7.1-full_build/bin/ffmpeg.exe'
    }

    try:
        # Videoni yuklab olish
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(video_info)

        # Audioni yuklab olish
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            audio_info = ydl.extract_info(url, download=True)
            audio_filename = os.path.join(DOWNLOADS_DIR, f"{audio_info['title']}.mp3")

        # Fayllarni yuborish
        await update.message.reply_video(video=open(video_filename, 'rb'))
        await update.message.reply_audio(audio=open(audio_filename, 'rb'))

        # Yuklangan fayllarni o'chirish
        if os.path.exists(video_filename):
            os.remove(video_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

        # Foydalanuvchi uchun muvaffaqiyatli xabar
        await update.message.reply_text("Video va audio muvaffaqiyatli jo'natildi!")

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {str(e)}")

    finally:
        # Fayllar o'chirilganidan keyin
        if os.path.exists(video_filename):
            os.remove(video_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)


def main():
    application = ApplicationBuilder().token("7900585023:AAHKTO0RqRtjWacyYgZZaitKnR8doTBge-o").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video_audio))

    application.run_polling()

if __name__ == '__main__':
    main()
