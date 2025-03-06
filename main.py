from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

COOKIES_FILE = "youtube.com_cookies.txt"  # Cookie fayli

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! YouTube linkni yuboring, men uni video yoki audio sifatida jo‘nataman.')

async def get_best_format(info):
    """Eng yaxshi formatni olish uchun yordamchi funksiya"""
    formats = info.get('formats', [])
    for f in formats:
        if f.get('acodec') != 'none' and f.get('vcodec') != 'none':  # Video + audio
            return f['url']
    return None  # Hech narsa topilmasa

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('🔄 Video yoki audio topilmoqda...')

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookies': COOKIES_FILE,  # Cookies bilan autentifikatsiya
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = await get_best_format(info)  # Eng yaxshi formatni olish

            if not video_url:
                await update.message.reply_text("⚠️ Video topilmadi yoki format mavjud emas!")
                return

        await update.message.reply_video(video=video_url, caption="🎥 Siz so‘ragan video")

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {str(e)}")

def main():
    application = ApplicationBuilder().token("7900585023:AAHKTO0RqRtjWacyYgZZaitKnR8doTBge-o").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))

    application.run_polling()

if __name__ == '__main__':
    main()
