from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
import yt_dlp
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! YouTube havolasini yuboring, men sizga video yoki audio faylni qaytaraman.\n\n🎬 Video uchun havolani to‘g‘ridan-to‘g‘ri yuboring.\n🎧 Audio uchun esa /audio buyrug‘idan foydalaning, so‘ngra havolani yuboring.")

# /audio komandasi - keyingi xabarni audio deb qabul qilish
async def audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['audio_mode'] = True
    await update.message.reply_text("🎧 Audio rejim yoqildi. Endi YouTube havolasini yuboring.")

# Havola kelganda video yoki audio yuklash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❌ Noto‘g‘ri URL. Iltimos, YouTube havolasini yuboring.")
        return

    await update.message.reply_text('⏳ Yuklab olinmoqda...')

    with tempfile.TemporaryDirectory() as temp_dir:
        # Audio rejimi yoqilgan bo‘lsa
        if context.user_data.get('audio_mode'):
            opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
            }
        else:
            opts = {
                'format': 'best',
                'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
            }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            # Fayl hajmini tekshirish
            if os.path.getsize(file_path) > 49 * 1024 * 1024:
                await update.message.reply_text("⚠️ Fayl hajmi 50MB dan katta. Telegram orqali yuborib bo‘lmaydi.")
                return

            with open(file_path, 'rb') as file:
                if context.user_data.get('audio_mode'):
                    await update.message.reply_audio(audio=file)
                    context.user_data['audio_mode'] = False  # audio rejimni o‘chir
                else:
                    await update.message.reply_video(video=file)

        except Exception as e:
            logging.exception("Xatolik yuz berdi")
            await update.message.reply_text(f"❌ Xatolik yuz berdi:\n{str(e)}")

def main():
    application = ApplicationBuilder().token("7900585023:AAHP4UmJnDo3_vEoN2i9mN-86nvkm281vvs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("audio", audio_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
