from telebot.types import ReplyKeyboardMarkup

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.setup_handlers()

    def setup_handlers(self):
        # هندلر برای دستور start
        @self.bot.message_handler(commands=['start'])
        def start_bot(message):
            reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            reply_keyboard.add('دریافت کد رهگیری', 'ارسال کد رهگیری')
            self.bot.send_message(message.chat.id, 'به بات تلگرامی خوش اومدی', reply_markup=reply_keyboard)
