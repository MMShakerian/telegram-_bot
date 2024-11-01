import re
import json
from telebot.types import Message, Document

class TrackingCodeAdminHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.orders_collection = db['order_code']
        self.admin_status = {}
        self.setup_handlers()

    def setup_handlers(self):
        # هندلر برای دکمه ارسال کد رهگیری
        @self.bot.message_handler(func=lambda message: message.text == 'ارسال کد رهگیری')
        def ask_for_json_upload(message):
            self.bot.send_message(message.chat.id, 'لطفا فایل JSON خود را آپلود کنید.')
            self.admin_status[message.chat.id] = 'waiting_for_json'

        # هندلر برای دریافت فایل JSON و بروزرسانی دیتابیس
        @self.bot.message_handler(content_types=['document'], func=lambda message: self.admin_status.get(message.chat.id) == 'waiting_for_json')
        def handle_json_upload(message: Message):
            file_info = self.bot.get_file(message.document.file_id)
            file = self.bot.download_file(file_info.file_path)
            
            try:
                # بارگذاری و پارس کردن فایل JSON
                data = json.loads(file.decode('utf-8'))
                
                # بروزرسانی اطلاعات در دیتابیس
                if isinstance(data, list):
                    self.orders_collection.insert_many(data)
                else:
                    self.orders_collection.insert_one(data)
                
                self.bot.send_message(message.chat.id, 'اطلاعات با موفقیت به دیتابیس اضافه شد.')
            except json.JSONDecodeError:
                self.bot.send_message(message.chat.id, 'فرمت فایل JSON نامعتبر است. لطفا یک فایل JSON معتبر ارسال کنید.')
            
            # پاکسازی وضعیت
            self.admin_status.pop(message.chat.id)
