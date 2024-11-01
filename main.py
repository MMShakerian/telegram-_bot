import telebot
from config import API_token
from command_handler import CommandHandler
from tracking_code_handler import TrackingCodeHandler
from pymongo import MongoClient
from whitraw import TrackingCodeAdminHandler

# ایجاد اتصال به دیتابیس
client = MongoClient("mongodb://localhost:27017")
db = client['post']  # نام دیتابیس را اینجا جایگزین کنید

# ایجاد بات تلگرام
bot = telebot.TeleBot(API_token)

# ایجاد نمونه‌ای از کلاس‌ها
command_handler = CommandHandler(bot)
tracking_code_handler = TrackingCodeHandler(bot, db)
whitraw = TrackingCodeAdminHandler(bot,db)

# شروع polling
bot.polling()
