from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasını yükler
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [["VIP Üyelik", "Sinyal Al"], ["Hesabım", "Yardım"]]
    await update.message.reply_text("Menüden seçin:", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "VIP Üyelik":  await update.message.reply_text("VIP akışı")
    elif t == "Sinyal Al": await update.message.reply_text("Sinyal akışı")
    elif t == "Hesabım":   await update.message.reply_text("Hesap bilgileri")
    elif t == "Yardım":    await update.message.reply_text("Yardım")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("BOT_TOKEN bulunamadı (.env dosyasını kontrol et)")
    app = ApplicationBuilder().token(TOKEN).read_timeout(30).write_timeout(30).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()
