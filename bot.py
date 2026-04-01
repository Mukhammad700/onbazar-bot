import os
import json
from telegram import Update, WebApp, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MINI_APP_URL = os.environ.get("MINI_APP_URL")
ADMIN_ID = 978942677

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(
        "🛍 Do'konni ochish",
        web_app=WebApp(url=MINI_APP_URL)
    )]]
    update.message.reply_text(
        "👋 Xush kelibsiz OnBazar ga!\n\nQuyidagi tugmani bosing 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_order(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    if data.get("action") == "order":
        items = data.get("items", [])
        total = data.get("total", 0)
        items_text = "\n".join([f"• {i['name']} x{i['qty']}" for i in items])
        update.message.reply_text(
            f"✅ Buyurtma qabul!\n\n{items_text}\n\n💰 Jami: {total:,} so'm"
        )
        user = update.message.from_user
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 Yangi buyurtma!\n👤 {user.full_name}\n📱 @{user.username or 'yoq'}\n\n{items_text}\n\n💰 {total:,} so'm"
        )

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.web_app_data, handle_order))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
