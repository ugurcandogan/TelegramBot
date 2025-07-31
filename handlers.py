from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_kb = [["Botu Başlat"]]
    await update.message.reply_text("Botu başlatmak için aşağıdaki butona tıklayın:", reply_markup=ReplyKeyboardMarkup(start_kb, resize_keyboard=True))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    main_kb = [["💎 VIP Üyelik", "🔍 Sinyal Tarama"], ["👤 Hesabım", "❓ Yardım"]]
    if t == "Botu Başlat":
        await update.message.reply_text("Menüden seçin:", reply_markup=ReplyKeyboardMarkup(main_kb, resize_keyboard=True))
    elif t == "💎 VIP Üyelik":
        await update.message.reply_text("VIP akışı")
    elif t == "🔍 Sinyal Tarama":
        await update.message.reply_text("Tarama başlatıldı 🔥")
        from scanner import get_signals_for_telegram
        # Sinyaller bulundukça anlık olarak yazdırılsın, en sonda özet mesajı gönderilsin
        await get_signals_for_telegram(send_to_channel=False, user_chat_id=update.effective_chat.id, user_bot=context.bot, only_summary='with_last')
    elif t == "👤 Hesabım":
        user = update.effective_user
        username = user.username if user.username else "Yok"
        telegram_id = user.id
        msg = f"Kullanıcı Adı: @{username}\nTelegram ID: `{telegram_id}`"
        await update.message.reply_text(msg, parse_mode="Markdown")
    elif t == "❓ Yardım":
        await update.message.reply_text("Yardım")
