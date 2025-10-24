import os
import json
import random
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv('BOT_TOKEN', '7575730725:AAE6n7LtUxRVmaiFwaBkfKgiwnt4tbuSeqM')
OWNER_ID = int(os.getenv('OWNER_ID', '7094827350'))

class PersianAIBot:
    def __init__(self):
        self.learning_data = self.load_learning_data()
        self.user_sessions = {}
        
    def load_learning_data(self):
        try:
            return {"qa": {}, "commands": {}}
        except:
            return {"qa": {}, "commands": {}}
    
    def save_learning_data(self):
        pass
    
    def is_owner(self, user_id):
        return user_id == OWNER_ID
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_sessions[user_id] = {"mode": "normal"}
        
        keyboard = [
            ["💬 چت هوشمند", "🧮 ماشین حساب"],
            ["🌤️ آب و هوا", "📚 دانشنامه"],
            ["😂 جوک", "💡 مشاوره"],
            ["🎯 یادگیری", "⚙️ تنظیمات"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = """
🤖 **به ربات هوش مصنوعی فارسی خوش آمدید!**

🔸 **امکانات ربات:**
• چت هوشمند فارسی
• ماشین حساب پیشرفته  
• اطلاعات آب و هوا
• دانشنامه فارسی
• جوک و مشاوره
• قابلیت یادگیری

📝 **فقط پیام بفرستید تا با شما صحبت کنم!**
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        if self.is_owner(user_id):
            owner_keyboard = [
                ["👑 مدیریت کاربران", "🔧 تنظیمات ویژه"],
                ["📊 آمار ربات", "🔄 ریست ربات"]
            ]
            owner_markup = ReplyKeyboardMarkup(owner_keyboard, resize_keyboard=True)
            await update.message.reply_text("👑 **دسترسی ویژه مالک فعال شد!**", reply_markup=owner_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
📖 **راهنمای ربات:**

💬 **چت هوشمند:** مستقیم پیام بفرستید
🧮 **ماشین حساب:** عبارت ریاضی مانند 2+3*5
🌤️ **آب و هوا:** نام شهر را بفرستید
📚 **دانشنامه:** موضوع مورد نظر را بپرسید
😂 **جوک:** جوک تصادفی فارسی
💡 **مشاوره:** نصیحت تصادفی

🎯 **یادگیری:** 
/learn سوال || پاسخ
        """
        await update.message.reply_text(help_text)

    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not context.args:
            await update.message.reply_text("🎯 **آموزش به ربات:**\n\nدستور: /learn سوال || پاسخ")
            return
        
        text = " ".join(context.args)
        if "||" not in text:
            await update.message.reply_text("❌ فرمت صحیح نیست. از || برای جدا کردن سوال و پاسخ استفاده کنید.")
            return
        
        question, answer = text.split("||", 1)
        question = question.strip()
        answer = answer.strip()
        
        self.learning_data["qa"][question] = answer
        await update.message.reply_text(f"✅ آموزش ثبت شد:\n\n**سوال:** {question}\n**پاسخ:** {answer}", parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {"mode": "normal"}
        
        if text in self.learning_data["qa"]:
            await update.message.reply_text(self.learning_data["qa"][text])
            return
        
        if text == "💬 چت هوشمند":
            await update.message.reply_text("💬 **حالت چت فعال شد!**\n\nهر پیامی بفرستید تا پاسخ هوشمند دریافت کنید.")
        
        elif text == "🧮 ماشین حساب":
            await update.message.reply_text("🧮 **ماشین حساب:**\n\nعبارت ریاضی مانند زیر بفرستید:\n2+3*5")
        
        elif text == "🌤️ آب و هوا":
            cities = ["تهران", "مشهد", "اصفهان", "شیراز", "تبریز"]
            keyboard = [[InlineKeyboardButton(city, callback_data=f"weather_{city}")] for city in cities]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("🌤️ **انتخاب شهر:**", reply_markup=reply_markup)
        
        elif text == "📚 دانشنامه":
            categories = ["ریاضی", "برنامه نویسی", "علم", "تاریخ"]
            keyboard = [[InlineKeyboardButton(cat, callback_data=f"knowledge_{cat}")] for cat in categories]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("📚 **انتخاب دسته:**", reply_markup=reply_markup)
        
        elif text == "😂 جوک":
            joke = self.get_persian_joke()
            await update.message.reply_text(f"😂 **جوک:**\n\n{joke}")
        
        elif text == "💡 مشاوره":
            advice = self.get_persian_advice()
            await update.message.reply_text(f"💡 **مشاوره:**\n\n{advice}")
        
        elif text == "🎯 یادگیری":
            await self.learn_command(update, context)
        
        elif text == "⚙️ تنظیمات" and self.is_owner(user_id):
            await update.message.reply_text("👑 **تنظیمات مالک:**\n\nاین بخش برای مدیریت ربات است.")
        
        elif text == "👑 مدیریت کاربران" and self.is_owner(user_id):
            user_count = len(self.user_sessions)
            await update.message.reply_text(f"📊 **آمار کاربران:**\n\nتعداد کاربران فعال: {user_count}")
        
        elif text == "📊 آمار ربات" and self.is_owner(user_id):
            learned_count = len(self.learning_data["qa"])
            user_count = len(self.user_sessions)
            await update.message.reply_text(f"📈 **آمار ربات:**\n\n👥 کاربران: {user_count}\n🎯 موارد آموخته: {learned_count}")
        
        else:
            response = self.generate_smart_response(text)
            await update.message.reply_text(response)

    def generate_smart_response(self, message):
        message_lower = message.lower()
        
        responses = {
            "سلام": "سلام! چطور می‌تونم کمک کنم؟ 😊",
            "حالت چطوره": "من یک ربات هستم، همیشه عالیم! شما چطورید؟",
            "اسمت چیه": "من یک دستیار هوش مصنوعی فارسی هستم! 🤖",
            "خداحافظ": "خداحافظ! موفق باشید 👋",
            "متشکرم": "خواهش می‌کنم! خوشحالم که مفید بودم 💫"
        }
        
        if message in responses:
            return responses[message]
        
        if any(op in message for op in ['+', '-', '*', '/', '×', '÷']):
            try:
                expr = message.replace('×', '*').replace('÷', '/').replace(' ', '')
                result = eval(expr)
                return f"🧮 نتیجه: {message} = {result}"
            except:
                return "❌ عبارت ریاضی نامعتبر است"
        
        return f"\"{message}\" - سوال جالبیه! 😊\n\nاز منوی پایین استفاده کنید."

    def get_persian_joke(self):
        jokes = [
            "چرا کامپیوتر نمی‌تونه قایم باشک بازی کنه؟ چون همیشه مونیتورش رو روشن می‌ذاره! 😄",
            "چرا برنامه‌نویس ها همیشه حالت عادی نمی‌تونن بخوابن؟ چون همیشه در حالت دیباگ هستن! 🐛"
        ]
        return random.choice(jokes)

    def get_persian_advice(self):
        advice_list = [
            "💡 همیشه قبل از انجام کار برنامه‌ریزی کن!",
            "🚀 یادگیری رو هیچوقت متوقف نکن"
        ]
        return random.choice(advice_list)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("weather_"):
            city = data.split("_")[1]
            weather_info = self.get_weather_for_city(city)
            await query.edit_message_text(weather_info)
        
        elif data.startswith("knowledge_"):
            category = data.split("_")[1]
            knowledge_info = self.get_knowledge_for_category(category)
            await query.edit_message_text(knowledge_info)

    def get_weather_for_city(self, city):
        weather_data = {
            "تهران": "🌤️ **آب و هوای تهران:**\n🌡 دما: 25°C\n📊 وضعیت: آفتابی\n💧 رطوبت: 40%",
            "مشهد": "🌤️ **آب و هوای مشهد:**\n🌡 دما: 22°C\n📊 وضعیت: نیمه ابری\n💧 رطوبت: 35%",
            "اصفهان": "🌤️ **آب و هوای اصفهان:**\n🌡 دما: 27°C\n📊 وضعیت: آفتابی\n💧 رطوبت: 30%",
            "شیراز": "🌤️ **آب و هوای شیراز:**\n🌡 دما: 29°C\n📊 وضعیت: گرم\n💧 رطوبت: 25%",
            "تبریز": "🌤️ **آب و هوای تبریز:**\n🌡 دما: 18°C\n📊 وضعیت: ابری\n💧 رطوبت: 45%"
        }
        return weather_data.get(city, "❌ اطلاعات این شهر موجود نیست")

    def get_knowledge_for_category(self, category):
        knowledge_data = {
            "ریاضی": "📐 **ریاضیات:**\n\n• مساحت دایره = π × شعاع²\n• محیط دایره = 2 × π × شعاع",
            "برنامه نویسی": "💻 **برنامه‌نویسی:**\n\n• پایتون: زبان سطح بالا\n• جاوا: زبان شیءگرا",
            "علم": "🔬 **علم:**\n\n• جاذبه: توسط نیوتن کشف شد\n• نسبیت: نظریه انیشتین",
            "تاریخ": "📜 **تاریخ:**\n\n• ایران: کشوری با تمدن کهن"
        }
        return knowledge_data.get(category, "❌ اطلاعات این دسته موجود نیست")

def main():
    bot = PersianAIBot()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("learn", bot.learn_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    print("🤖 Bot is running on Render...")
    application.run_polling()

if __name__ == "__main__":
    main()
