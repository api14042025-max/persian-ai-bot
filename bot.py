import os
import json
import random
import requests
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv('BOT_TOKEN', '7575730725:AAE6n7LtUxRVmaiFwaBkfKgiwnt4tbuSeqM')
OWNER_ID = int(os.getenv('OWNER_ID', '7094827350'))

class AdvancedAI:
    def __init__(self):
        self.user_profiles = {}
        self.conversation_memory = {}
        self.emotion_data = {}
        
    def is_owner(self, user_id):
        return user_id == OWNER_ID

    def analyze_emotion(self, text):
        """تجزیه و تحلیل احساسات متن"""
        text_lower = text.lower()
        positive_words = ['خوب', 'عالی', 'عالیه', 'ممنون', 'تشکر', 'خوشحال', 'شاد']
        negative_words = ['بد', 'بدی', 'ناراحت', 'غمگین', 'عصبانی', 'خسته']
        
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        if positive_score > negative_score:
            return "شاد 😊", "مثبت"
        elif negative_score > positive_score:
            return "ناراحت 😔", "منفی"
        else:
            return "عادی 😐", "خنثی"

    def get_contextual_response(self, message, user_id):
        """پاسخ هوشمند بر اساس زمینه و حافظه"""
        message_lower = message.lower()
        
        # تحلیل زمینه گفتگو
        context_keywords = {
            "سلام": "سلام! چطور می‌تونم کمک کنم؟ امروز حالتون چطوره؟ 😊",
            "حال": "من یک هوش مصنوعی پیشرفته هستم! همیشه آماده کمک کردنم. شما چطورید؟ 🤖",
            "اسم": "من یک AI فارسی هستم! می‌تونید من رو 'هوشمند' صدا کنید 🧠",
            "هوش": "من با تکنولوژی GPT-like کار می‌کنم و دائماً در حال یادگیری هستم! 💫",
            "یادگیری": "من از هر گفتگو یاد می‌گیرم و خودم رو بهبود می‌دم! 📚"
        }
        
        for keyword, response in context_keywords.items():
            if keyword in message_lower:
                return response
        
        # پاسخ‌های هوشمند پیشرفته
        if "چطور" in message_lower or "چگونه" in message_lower:
            return f"برای '{message}' می‌تونم راهنماییتون کنم! نیاز به اطلاعات خاصی دارید؟ 🎯"
        
        elif "چرا" in message_lower:
            return "سوال فلسفی جالبی پرسیدید! می‌خواید عمیق‌تر بررسیش کنیم؟ 💭"
        
        elif "برنامه" in message_lower or "کد" in message_lower:
            return "در زمینه برنامه‌نویسی می‌تونم کمک کنم! پایتون، وب، هوش مصنوعی... 💻"
        
        elif "ریاضی" in message_lower:
            return "ریاضیات تخصص منه! از جبر تا محاسبات پیچیده 🧮"
        
        elif "آینده" in message_lower:
            predictions = [
                "فکر می‌کنم در آینده تکنولوژی بیشتر زندگی ما رو تحت تاثیر قرار بده! 🚀",
                "به نظرم هوش مصنوعی تو همه زمینه‌ها پیشرفت می‌کنه! 🤖",
                "فکر می‌کنم انسان‌ها بیشتر با AI همکاری می‌کنن! 💫"
            ]
            return random.choice(predictions)
        
        else:
            # پاسخ خلاقانه
            creative_responses = [
                f"'{message}' - سوال جالبیه! فکر کنم می‌تونیم از زوایای مختلف بررسیش کنیم! 🔍",
                f"در مورد '{message}' نظرات مختلفی وجود داره! می‌خواید بحث کنیم؟ 💬",
                f"این موضوع رو می‌شه به روش‌های مختلف تحلیل کرد! نظر شما چیه؟ 🤔",
                f"جالبه! می‌تونم اطلاعات بیشتری در این زمینه بهتون بدم! 📚"
            ]
            return random.choice(creative_responses)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        # ایجاد پروفایل کاربر
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "name": update.effective_user.first_name,
                "join_date": datetime.now(),
                "message_count": 0,
                "emotion_history": []
            }
        
        keyboard = [
            ["🧠 چت هوشمند", "📊 تحلیل احساسات"],
            ["🎯 پیش‌بینی", "🔍 جستجوی پیشرفته"],
            ["📈 آمار کاربری", "🎮 تست هوش"],
            ["⚡ محاسبات پیچیده", "👑 ویژه مالک"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = """
🧠 **به هوش مصنوعی پیشرفته خوش آمدید!**

✨ **قابلیت‌های پیشرفته:**
• تحلیل احساسات و متن‌کاوی
• حافظه گفتگو
• پیش‌بینی هوشمند
• جستجوی پیشرفته
• تست‌های روان‌شناسی
• محاسبات پیچیده
• آمار کاربری پیشرفته

🤖 **من دائماً در حال یادگیری هستم!**
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        if self.is_owner(user_id):
            await update.message.reply_text("👑 **دسترسی ویژه مالک فعال شد!**")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        # آپدیت پروفایل کاربر
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "name": update.effective_user.first_name,
                "join_date": datetime.now(),
                "message_count": 0,
                "emotion_history": []
            }
        
        self.user_profiles[user_id]["message_count"] += 1
        
        # تحلیل احساسات
        emotion, score = self.analyze_emotion(text)
        self.user_profiles[user_id]["emotion_history"].append({
            "text": text,
            "emotion": emotion,
            "score": score,
            "timestamp": datetime.now()
        })
        
        if text == "🧠 چت هوشمند":
            await update.message.reply_text("🧠 **حالت چت پیشرفته فعال شد!**\n\nهر پیامی بفرستید تا پاسخ هوشمند دریافت کنید!")
        
        elif text == "📊 تحلیل احساسات":
            emotion_stats = self.get_emotion_stats(user_id)
            await update.message.reply_text(f"📊 **تحلیل احساسات شما:**\n\n{emotion_stats}")
        
        elif text == "🎯 پیش‌بینی":
            prediction = self.generate_prediction()
            await update.message.reply_text(f"🎯 **پیش‌بینی هوشمند:**\n\n{prediction}")
        
        elif text == "🔍 جستجوی پیشرفته":
            await update.message.reply_text("🔍 **جستجوی پیشرفته:**\n\nموضوع مورد نظر را تایپ کنید...")
        
        elif text == "📈 آمار کاربری":
            stats = self.get_user_stats(user_id)
            await update.message.reply_text(f"📈 **آمار کاربری شما:**\n\n{stats}")
        
        elif text == "🎮 تست هوش":
            await self.iq_test(update, context)
        
        elif text == "⚡ محاسبات پیچیده":
            await update.message.reply_text("⚡ **محاسبات پیچیده:**\n\nعبارت ریاضی پیچیده وارد کنید...")
        
        elif text == "👑 ویژه مالک" and self.is_owner(user_id):
            await self.owner_dashboard(update, context)
        
        else:
            # پاسخ هوشمند پیشرفته
            response = self.get_contextual_response(text, user_id)
            await update.message.reply_text(response)

    def get_emotion_stats(self, user_id):
        """آمار احساسات کاربر"""
        if user_id not in self.user_profiles:
            return "اطلاعاتی موجود نیست"
        
        emotions = [entry["score"] for entry in self.user_profiles[user_id]["emotion_history"][-10:]]
        positive = emotions.count("مثبت")
        negative = emotions.count("منفی")
        neutral = emotions.count("خنثی")
        
        return (
            f"😊 مثبت: {positive}\n"
            f"😔 منفی: {negative}\n"
            f"😐 خنثی: {neutral}\n\n"
            f"📊 آخرین تحلیل: {self.user_profiles[user_id]['emotion_history'][-1]['emotion']}"
        )

    def generate_prediction(self):
        """پیش‌بینی هوشمند"""
        predictions = [
            "فردا روز خوبی برای یادگیری چیزهای جدید خواهد بود! 📚",
            "به زودی فرصت‌های جدیدی در زندگی شما ظاهر می‌شود! 💫",
            "هفته آینده زمان مناسبی برای شروع پروژه‌های جدید است! 🚀",
            "به زودی با افراد جدید و جالبی آشنا خواهید شد! 👥",
            "انرژی مثبت زیادی در راه است! آماده موفقیت باشید! 🌟"
        ]
        return random.choice(predictions)

    def get_user_stats(self, user_id):
        """آمار کاربری پیشرفته"""
        if user_id not in self.user_profiles:
            return "کاربر جدید"
        
        profile = self.user_profiles[user_id]
        days_joined = (datetime.now() - profile["join_date"]).days
        
        return (
            f"👤 نام: {profile['name']}\n"
            f"📅 عضو شده: {days_joined} روز پیش\n"
            f"💬 تعداد پیام: {profile['message_count']}\n"
            f"📈 میانگین روزانه: {profile['message_count'] / max(days_joined, 1):.1f} پیام\n"
            f"🎯 فعالیت: {'عالی' if profile['message_count'] > 50 else 'خوب' if profile['message_count'] > 20 else 'معمولی'}"
        )

    async def iq_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تست هوش"""
        questions = [
            {
                "question": "اگر ۲ ماشین ۲ ساعت وقت نیاز داشته باشند تا ۲ دستگاه رو بسازن، ۴ ماشین چقدر وقت نیاز دارن تا ۴ دستگاه بسازن؟",
                "options": ["۲ ساعت", "۴ ساعت", "۱ ساعت", "۸ ساعت"],
                "answer": 0
            },
            {
                "question": "کدوم گزینه با بقیه فرق داره؟",
                "options": ["مثلث", "مربع", "دایره", "مکعب"],
                "answer": 3
            }
        ]
        
        q = random.choice(questions)
        keyboard = [[InlineKeyboardButton(opt, callback_data=f"iq_{i}")] for i, opt in enumerate(q["options"])]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.user_data["current_iq"] = q
        await update.message.reply_text(f"🧠 **تست هوش:**\n\n{q['question']}", reply_markup=reply_markup)

    async def owner_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """داشبورد مالک"""
        total_users = len(self.user_profiles)
        total_messages = sum(user["message_count"] for user in self.user_profiles.values())
        
        keyboard = [
            [InlineKeyboardButton("📊 آمار کامل", callback_data="stats_full")],
            [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="users_manage")],
            [InlineKeyboardButton("🧠 آنالیز داده", callback_data="data_analyze")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👑 **داشبورد مالک:**\n\n"
            f"👥 کاربران کل: {total_users}\n"
            f"💬 پیام‌های کل: {total_messages}\n"
            f"📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("iq_"):
            answer_index = int(data.split("_")[1])
            current_iq = context.user_data.get("current_iq")
            
            if current_iq and answer_index == current_iq["answer"]:
                await query.edit_message_text("✅ **درست جواب دادید! شما باهوش هستید!** 🧠")
            else:
                await query.edit_message_text("❌ **پاسخ صحیح نبود! بازم تلاش کنید!** 💪")
        
        elif data == "stats_full":
            total_users = len(self.user_profiles)
            await query.edit_message_text(f"📊 **آمار کامل:**\n\nکاربران فعال: {total_users}")
        
        elif data == "users_manage":
            await query.edit_message_text("👥 **مدیریت کاربران:**\n\nاین بخش برای مدیریت پیشرفته کاربران است")

def main():
    ai_bot = AdvancedAI()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", ai_bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_bot.handle_message))
    application.add_handler(CallbackQueryHandler(ai_bot.handle_callback))
    
    print("🧠 هوش مصنوعی پیشرفته در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
