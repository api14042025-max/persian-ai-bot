import os
import random
import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

BOT_TOKEN = os.getenv('BOT_TOKEN', '7575730725:AAE6n7LtUxRVmaiFwaBkfKgiwnt4tbuSeqM')
OWNER_ID = int(os.getenv('OWNER_ID', '7094827350'))

class HorefaiBot:
    def __init__(self):
        self.user_scores = {}
        self.games = {}
        
    def is_owner(self, user_id):
        return user_id == OWNER_ID

    async def start(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        
        keyboard = [
            ["🎮 بازی ها", "😂 هَرفه"],
            ["🎵 موزیک", "📊 امتیاز من"],
            ["🎲 شانس", "🔥 چلنج"],
            ["👑 ویژه مالک"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = """
🤪 **به ربات هَرفه‌ای خوش اومدی!**

🃏 **قابلیت‌های باحال:**
• بازی‌های فان 🎮
• جوک‌های هَرفه 😂
• موزیک رندوم 🎵
• چلنج‌های باحال 🔥
• سیستم امتیاز 📊

**بیا خوش بگذرونیم!** 🎉
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        if self.is_owner(user_id):
            await update.message.reply_text("👑 **مالک عزیز! دسترسی ویژه فعال شد!**")

    async def handle_message(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        text = update.message.text
        
        if text == "🎮 بازی ها":
            await self.show_games(update, context)
        
        elif text == "😂 هَرفه":
            await self.send_horef(update, context)
        
        elif text == "🎵 موزیک":
            await self.send_music(update, context)
        
        elif text == "📊 امتیاز من":
            await self.show_score(update, context)
        
        elif text == "🎲 شانس":
            await self.luck_game(update, context)
        
        elif text == "🔥 چلنج":
            await self.challenge(update, context)
        
        elif text == "👑 ویژه مالک" and self.is_owner(user_id):
            await self.owner_features(update, context)
        
        else:
            await self.random_response(update, context)

    async def show_games(self, update: Update, context: CallbackContext):
        keyboard = [
            [InlineKeyboardButton("🎯 حدس عدد", callback_data="game_guess")],
            [InlineKeyboardButton("🎲 تاس بازی", callback_data="game_dice")],
            [InlineKeyboardButton("✂️ سنگ کاغذ قیچی", callback_data="game_rps")],
            [InlineKeyboardButton("🧠 معما", callback_data="game_riddle")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🎮 **انتخاب بازی:**", reply_markup=reply_markup)

    async def send_horef(self, update: Update, context: CallbackContext):
        horef_list = [
            "😂 چرا مرغ تو کامپیوتر نمی‌ره؟ چون می‌ترسه ویروس بگیره! 🐔",
            "🤣 چرا گوسفند برنامه‌نویس شد؟ چون می‌خواست بَهِهِهِهِهِ کد بزنه! 🐑",
            "😆 چرا موز تو کامپیوتر کار نمی‌کنه؟ چون پورت USB نداشت! 🍌",
            "🎪 یه دایناسور رفت دکتر، دکتر گفت: باید بری متخصص کامپیوتر، مشکلت ویندوز قدیمیه! 🦖",
            "🤪 چرا کتاب ریاضی تو مهمونی نمی‌رقصید؟ چون می‌گفت من فقط می‌تونم انتگرال برقصم! 📚"
        ]
        horef = random.choice(horef_list)
        await update.message.reply_text(f"**هورفه:**\n\n{horef}")

    async def send_music(self, update: Update, context: CallbackContext):
        songs = [
            "🎵 **آهنگ تصادفی:**\n\n'یه روز قشنگ میاد' - با صدای ربات هَرفه‌ای! 🎤",
            "🎶 **آهنگ تصادفی:**\n\n'کد میزنم تا صبح' - سبک: برنامه‌نویسی راک! 🎸",
            "🎧 **آهنگ تصادفی:**\n\n'بَگِ عاشقانه' - تنظیم: کامپایلر قلب! 💓",
            "📻 **آهنگ تصادفی:**\n\n'الگوریتم عشق' - خواننده: هوش مصنوعی! 🤖"
        ]
        song = random.choice(songs)
        await update.message.reply_text(song)

    async def show_score(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        score = self.user_scores.get(user_id, 0)
        
        level = "تازه‌کار" if score < 10 else "حرفه‌ای" if score < 50 else "اَبر قهرمان"
        
        await update.message.reply_text(
            f"📊 **کاربر:** {update.effective_user.first_name}\n"
            f"🏆 **امتیاز:** {score}\n"
            f"⭐ **سطح:** {level}\n\n"
            f"با بازی کردن امتیاز بگیر! 🎯"
        )

    async def luck_game(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        
        luck_options = [
            ("🍀 امروز روز شانسی!", 5),
            ("💰 برنده ۱۰۰۰ سکه شدی!", 10),
            ("🎁 یک هدیه رایگان!", 8),
            ("⭐ امتیاز ویژه!", 7),
            ("🤝 شانس دوست‌یابی!", 3)
        ]
        
        result, points = random.choice(luck_options)
        self.user_scores[user_id] = self.user_scores.get(user_id, 0) + points
        
        await update.message.reply_text(
            f"🎲 **گردونه شانس:**\n\n"
            f"{result}\n"
            f"➕ {points} امتیاز گرفتی!\n"
            f"💰 مجموع امتیاز: {self.user_scores[user_id]}"
        )

    async def challenge(self, update: Update, context: CallbackContext):
        challenges = [
            "🔥 **چلنج:** یه جوک هَرفه بگو!",
            "💪 **چلنج:** اسم ۵ تا میوه رو بگو که با 'پ' شروع میشن!",
            "🎯 **چلنج:** عدد بین ۱ تا ۱۰ رو حدس بزن!",
            "🤔 **چلنج:** معما: چی هست که می‌پره اما پر نداره؟",
            "🎪 **چلنج:** یه داستان کوتاه ۲ خطی بساز!"
        ]
        
        challenge = random.choice(challenges)
        await update.message.reply_text(challenge)

    async def owner_features(self, update: Update, context: CallbackContext):
        keyboard = [
            [InlineKeyboardButton("🎪 همه رو خوشحال کن", callback_data="owner_happy")],
            [InlineKeyboardButton("📊 آمار ربات", callback_data="owner_stats")],
            [InlineKeyboardButton("🎁 هدیه به همه", callback_data="owner_gift")],
            [InlineKeyboardButton("🔊 اعلامیه", callback_data="owner_announce")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("👑 **منوی ویژه مالک:**", reply_markup=reply_markup)

    async def random_response(self, update: Update, context: CallbackContext):
        responses = [
            "🤔 باحال گفتی! داری چیکار میکنی؟",
            "🎪 وای! این حرفت رو باید توی موزه هَرفه‌ها بذارم!",
            "😂 دمت گرم! حال کردم!",
            "🎯 حرف باحالی زدی! می‌خوای بازی کنیم؟",
            "🤖 من که هوش مصنوعی هستم، اما از حرفت خوشم اومد!",
            "🎊 عالیه! ادامه بده!",
            "💫 واو! این رو انتظار نداشتم!",
            "🎪 تو استعداد داری تو هَرفه بازی!"
        ]
        response = random.choice(responses)
        await update.message.reply_text(response)

    async def handle_callback(self, update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "game_guess":
            await query.edit_message_text("🎯 **حدس عدد:**\n\nبین ۱ تا ۱۰ یه عدد بگو!")
        
        elif data == "game_dice":
            dice = random.randint(1, 6)
            await query.edit_message_text(f"🎲 **تاس بازی:**\n\nعدد تو: {dice}")
        
        elif data == "game_rps":
            await query.edit_message_text("✂️ **سنگ کاغذ قیچی:**\n\nسنگ، کاغذ یا قیچی؟")
        
        elif data == "game_riddle":
            riddles = [
                "🧠 **معما:** چی هست که هر چی بیشترش رو برداریم، بزرگ‌تر میشه؟",
                "🤔 **معما:** چی می‌پره اما پر نداره؟",
                "💭 **معما:** چی رو می‌شکنیم اما استفاده می‌کنیم؟"
            ]
            riddle = random.choice(riddles)
            await query.edit_message_text(riddle)
        
        elif data == "owner_happy":
            await query.edit_message_text("🎉 **همه کاربران رو خوشحال کردی!**\n\n➕ ۵ امتیاز به همه!")
        
        elif data == "owner_stats":
            user_count = len(self.user_scores)
            total_score = sum(self.user_scores.values())
            await query.edit_message_text(f"📈 **آمار ربات:**\n\n👥 کاربران: {user_count}\n🏆 مجموع امتیازها: {total_score}")
        
        elif data == "owner_gift":
            await query.edit_message_text("🎁 **به همه کاربران هدیه دادی!**\n\nهمه ۱۰ امتیاز گرفتن!")
        
        elif data == "owner_announce":
            await query.edit_message_text("📢 **اعلامیه:**\n\nربات هَرفه‌ای آماده خدمت‌رسانی! 🎪")

def main():
    bot = HorefaiBot()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    print("🎪 ربات هَرفه‌ای در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
