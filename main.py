from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! YouTube linkni yuboring, men uni video yoki audio sifatida jo‘nataman.')

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('🔄 Video yoki audio topilmoqda...')

    ydl_opts_video = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=False)  # Faqat URL olish
            video_url = info['url']  # Video fayl URL'ini olish

        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']  # Audio fayl URL'ini olish

        # Foydalanuvchiga video va audiolarni jo‘natish
        await update.message.reply_video(video=video_url, caption="🎥 Siz so‘ragan video")
        await update.message.reply_audio(audio=audio_url, caption="🎵 Siz so‘ragan audio")

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {str(e)}")

def main():
    application = ApplicationBuilder().token("7900585023:AAHKTO0RqRtjWacyYgZZaitKnR8doTBge-o").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))

    application.run_polling()

if __name__ == '__main__':
    main()
