from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasını yükler
TOKEN = os.getenv("BOT_TOKEN")


from handlers import start, handle_buttons

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("BOT_TOKEN bulunamadı (.env dosyasını kontrol et)")
    app = ApplicationBuilder().token(TOKEN).read_timeout(30).write_timeout(30).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()
