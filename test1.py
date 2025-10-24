from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json
import random
from datetime import datetime
import os

# Bot configuration
BOT_TOKEN = "7575730725:AAE6n7LtUxRVmaiFwaBkfKgiwnt4tbuSeqM"
OWNER_ID = 7094827350  # Your user ID

class PersianAIBot:
    def __init__(self):
        self.learning_data = self.load_learning_data()
        self.user_sessions = {}
        
    def load_learning_data(self):
        """Load learning data from file"""
        try:
            with open('learning_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"qa": {}, "commands": {}}
    
    def save_learning_data(self):
        """Save learning data to file"""
        try:
            with open('learning_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to save learning data: {e}")
    
    def is_owner(self, user_id):
        """Check if user is owner"""
        return user_id == OWNER_ID
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_sessions[user_id] = {"mode": "normal"}
        
        # Create Persian keyboard
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

🔸 **دستورات:**
/start - شروع ربات
/help - راهنما
/learn - آموزش به ربات

📝 **فقط پیام بفرستید تا با شما صحبت کنم!**
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        # Show owner menu if user is owner
        if self.is_owner(user_id):
            owner_keyboard = [
                ["👑 مدیریت کاربران", "🔧 تنظیمات ویژه"],
                ["📊 آمار ربات", "🔄 ریست ربات"]
            ]
            owner_markup = ReplyKeyboardMarkup(owner_keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "👑 **دسترسی ویژه مالک فعال شد!**\n\n"
                "امکانات مدیریتی در دسترس است.",
                reply_markup=owner_markup
            )

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
مثال: /learn پایتون چیست؟ || یک زبان برنامه نویسی

⚙️ **تنظیمات مالک:** (فقط برای مالک)
• مدیریت کاربران
• مشاهده آمار
• ریست ربات
        """
        await update.message.reply_text(help_text)

    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not context.args:
            await update.message.reply_text(
                "🎯 **آموزش به ربات:**\n\n"
                "دستور: /learn سوال || پاسخ\n\n"
                "مثال:\n"
                "/learn پایتون چیست؟ || یک زبان برنامه نویسی\n"
                "/learn اسم تو چیست؟ || من یک ربات هوش مصنوعی هستم"
            )
            return
        
        text = " ".join(context.args)
        if "||" not in text:
            await update.message.reply_text("❌ فرمت صحیح نیست. از || برای جدا کردن سوال و پاسخ استفاده کنید.")
            return
        
        question, answer = text.split("||", 1)
        question = question.strip()
        answer = answer.strip()
        
        self.learning_data["qa"][question] = answer
        self.save_learning_data()
        
        await update.message.reply_text(f"✅ آموزش ثبت شد:\n\n**سوال:** {question}\n**پاسخ:** {answer}", parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {"mode": "normal"}
        
        # Check learned responses first
        if text in self.learning_data["qa"]:
            await update.message.reply_text(self.learning_data["qa"][text])
            return
        
        # Handle keyboard buttons
        if text == "💬 چت هوشمند":
            await update.message.reply_text("💬 **حالت چت فعال شد!**\n\nهر پیامی بفرستید تا پاسخ هوشمند دریافت کنید.")
        
        elif text == "🧮 ماشین حساب":
            await update.message.reply_text("🧮 **ماشین حساب:**\n\nعبارت ریاضی مانند زیر بفرستید:\n2+3*5\n(5+8)*2\n10/2")
        
        elif text == "🌤️ آب و هوا":
            cities = ["تهران", "مشهد", "اصفهان", "شیراز", "تبریز"]
            keyboard = [[InlineKeyboardButton(city, callback_data=f"weather_{city}")] for city in cities]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("🌤️ **انتخاب شهر:**", reply_markup=reply_markup)
        
        elif text == "📚 دانشنامه":
            categories = ["ریاضی", "برنامه نویسی", "علم", "تاریخ", "فرهنگ"]
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
        
        elif text == "⚙️ تنظیمات":
            if self.is_owner(user_id):
                await self.owner_settings(update, context)
            else:
                await update.message.reply_text("❌ این بخش فقط برای مالک ربات قابل دسترسی است.")
        
        # Owner only commands
        elif text == "👑 مدیریت کاربران" and self.is_owner(user_id):
            await self.manage_users(update, context)
        
        elif text == "🔧 تنظیمات ویژه" and self.is_owner(user_id):
            await self.special_settings(update, context)
        
        elif text == "📊 آمار ربات" and self.is_owner(user_id):
            await self.bot_stats(update, context)
        
        elif text == "🔄 ریست ربات" and self.is_owner(user_id):
            await self.reset_bot(update, context)
        
        else:
            # Smart response for other messages
            response = self.generate_smart_response(text)
            await update.message.reply_text(response)

    def generate_smart_response(self, message):
        """Generate intelligent Persian response"""
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
        
        # Math calculation
        if any(op in message for op in ['+', '-', '*', '/', '×', '÷']):
            try:
                expr = message.replace('×', '*').replace('÷', '/').replace(' ', '')
                result = eval(expr)
                return f"🧮 نتیجه: {message} = {result}"
            except:
                return "❌ عبارت ریاضی نامعتبر است"
        
        # Weather query
        if "آب و هوا" in message_lower:
            return "🌤️ لطفاً نام شهر را بفرستید یا از دکمه آب و هوا استفاده کنید"
        
        # Default response
        return f"\"{message}\" - سوال جالبیه! 😊\n\nمی‌تونم در زمینه‌های مختلف کمک کنم. از منوی پایین استفاده کنید یا سوالتون رو دقیق‌تر بپرسید."

    def get_persian_joke(self):
        jokes = [
            "چرا کامپیوتر نمی‌تونه قایم باشک بازی کنه؟ چون همیشه مونیتورش رو روشن می‌ذاره! 😄",
            "چرا برنامه‌نویس ها همیشه حالت عادی نمی‌تونن بخوابن؟ چون همیشه در حالت دیباگ هستن! 🐛",
            "چرا کتاب ریاضی غمگین بود؟ چون مشکل زیادی داشت! 📚"
        ]
        return random.choice(jokes)

    def get_persian_advice(self):
        advice_list = [
            "💡 همیشه قبل از انجام کار برنامه‌ریزی کن!",
            "🚀 یادگیری رو هیچوقت متوقف نکن", 
            "💪 برای هر مشکلی راه‌حلی وجود داره!",
            "🌟 امروز بهترین روز برای شروع یک کار جدیده"
        ]
        return random.choice(advice_list)

    # Owner only functions
    async def owner_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("📊 آمار کاربران", callback_data="stats_users")],
            [InlineKeyboardButton("🗑 پاک کردن حافظه", callback_data="clear_memory")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("👑 **تنظیمات مالک:**", reply_markup=reply_markup)

    async def manage_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_count = len(self.user_sessions)
        await update.message.reply_text(f"📊 **آمار کاربران:**\n\nتعداد کاربران فعال: {user_count}")

    async def special_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔧 **تنظیمات ویژه مالک:**\n\nاین بخش برای مدیریت پیشرفته ربات است.")

    async def bot_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        learned_count = len(self.learning_data["qa"])
        user_count = len(self.user_sessions)
        await update.message.reply_text(
            f"📈 **آمار ربات:**\n\n"
            f"👥 کاربران فعال: {user_count}\n"
            f"🎯 موارد آموخته شده: {learned_count}\n"
            f"🕒 زمان فعالیت: فعال"
        )

    async def reset_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("✅ بله، ریست کن", callback_data="confirm_reset")],
            [InlineKeyboardButton("❌ خیر", callback_data="cancel_reset")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("⚠️ **ریست ربات:**\n\nآیا مطمئن هستید؟", reply_markup=reply_markup)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        if data.startswith("weather_"):
            city = data.split("_")[1]
            weather_info = self.get_weather_for_city(city)
            await query.edit_message_text(weather_info)
        
        elif data.startswith("knowledge_"):
            category = data.split("_")[1]
            knowledge_info = self.get_knowledge_for_category(category)
            await query.edit_message_text(knowledge_info)
        
        elif data == "stats_users" and self.is_owner(user_id):
            user_count = len(self.user_sessions)
            await query.edit_message_text(f"👥 **آمار کاربران:**\n\nتعداد کاربران فعال: {user_count}")
        
        elif data == "confirm_reset" and self.is_owner(user_id):
            self.learning_data = {"qa": {}, "commands": {}}
            self.save_learning_data()
            await query.edit_message_text("✅ **ربات با موفقیت ریست شد!**")
        
        elif data == "cancel_reset":
            await query.edit_message_text("❌ **ریست لغو شد.**")
        
        elif data == "back_main":
            await query.edit_message_text("🔙 به منوی اصلی بازگشتید.")

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
            "ریاضی": "📐 **ریاضیات:**\n\n• مساحت دایره = π × شعاع²\n• محیط دایره = 2 × π × شعاع\n• قضیه فیثاغورث: a² + b² = c²",
            "برنامه نویسی": "💻 **برنامه‌نویسی:**\n\n• پایتون: زبان سطح بالا\n• جاوا: زبان شیءگرا\n• HTML: زبان نشانه‌گذاری وب",
            "علم": "🔬 **علم:**\n\n• جاذبه: توسط نیوتن کشف شد\n• نسبیت: نظریه انیشتین\n• DNA: حاوی اطلاعات ژنتیکی",
            "تاریخ": "📜 **تاریخ:**\n\n• ایران: کشوری با تمدن کهن\n• کوروش: بنیانگذار امپراتوری هخامنشی",
            "فرهنگ": "🎭 **فرهنگ:**\n\n• نوروز: سال نو ایرانی\n• هنر: مینیاتور، فرش، موسیقی"
        }
        return knowledge_data.get(category, "❌ اطلاعات این دسته موجود نیست")

def main():
    bot = PersianAIBot()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("learn", bot.learn_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    print("=" * 50)
    print("🤖 PERSIAN AI TELEGRAM BOT")
    print("=" * 50)
    print("✅ Bot is running...")
    print("📍 All messages in Telegram will be in PERSIAN")
    print("👑 Owner ID:", OWNER_ID)
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    application.run_polling()

if __name__ == "__main__":
    main()
