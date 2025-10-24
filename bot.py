import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN', '7575730725:AAE6n7LtUxRVmaiFwaBkfKgiwnt4tbuSeqM')
OWNER_ID = int(os.getenv('OWNER_ID', '7094827350'))

class PersianAIBot:
    def __init__(self):
        self.learning_data = {"qa": {}}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [["💬 چت هوشمند", "🧮 ماشین حساب"], ["🌤️ آب و هوا", "📚 دانشنامه"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🤖 به ربات خوش آمدید!", reply_markup=reply_markup)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "💬 چت هوشمند":
            await update.message.reply_text("💬 چت فعال شد!")
        else:
            await update.message.reply_text(f"'{text}' - سوال جالبیه! 😊")

def main():
    bot = PersianAIBot()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    print("🤖 Bot is running on Render...")
    application.run_polling()

if __name__ == "__main__":
    main()
