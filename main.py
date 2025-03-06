from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
import yt_dlp
import tempfile
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! YouTube linkini yuboring.")

async def download_video_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('Yuklanmoqda...')

    with tempfile.TemporaryDirectory() as temp_dir:
        video_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
        }

        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg',
        }

        try:
            # Videoni yuklab olish
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                video_path = ydl.prepare_filename(video_info)

            # Audioni yuklab olish
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                audio_info = ydl.extract_info(url, download=True)
                audio_path = ydl.prepare_filename(audio_info).replace('.webm', '.mp3')

            # Fayllarni yuborish
            with open(video_path, 'rb') as video_file, open(audio_path, 'rb') as audio_file:
                await update.message.reply_video(video=video_file)
                await update.message.reply_audio(audio=audio_file)

        except Exception as e:
            await update.message.reply_text(f"Xatolik: {str(e)}")

def main():
    application = ApplicationBuilder().token("7900585023:AAHKTO0RqRtjWacyYgZZaitKnR8doTBge-o").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video_audio))
    application.run_polling()

if __name__ == '__main__':
    main()
