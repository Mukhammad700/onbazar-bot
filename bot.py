import os, json
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MINI_APP_URL = os.environ.get("MINI_APP_URL")
ADMIN_ID = 978942677

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛍 Do'konni ochish", web_app=WebAppInfo(url=MINI_APP_URL))]]
    await update.message.reply_text(
        "👋 Xush kelibsiz OnBazar ga!\n\nQuyidagi tugmani bosing 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)
    if data.get("action") == "order":
        items = data.get("items", [])
        total = data.get("total", 0)
        items_text = "\n".join([f"• {i['name']} x{i['qty']}" for i in items])
        await update.message.reply_text(
            f"✅ Buyurtma qabul!\n\n{items_text}\n\n💰 Jami: {total:,} so'm"
        )
        user = update.message.from_user
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 Yangi buyurtma!\n👤 {user.full_name}\n📱 @{user.username or 'yoq'}\n\n{items_text}\n\n💰 {total:,} so'm"
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_order))
app.run_polling()
