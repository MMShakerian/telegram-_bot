import re
from telebot.types import Message

class TrackingCodeHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.orders_collection = db['order_code']
        self.user_status = {}
        self.date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        self.setup_handlers()

    def setup_handlers(self):
        # هندلر برای دکمه دریافت کد رهگیری
        @self.bot.message_handler(func=lambda message: message.text == 'دریافت کد رهگیری')
        def ask_for_order_date(message):
            self.bot.send_message(message.chat.id, 'لطفا تاریخ ثبت سفارش خود را به صورت فرمت زیر بنویسید:\nYYYY-MM-DD')
            self.user_status[message.chat.id] = 'waiting_for_date'

        # هندلر برای دریافت و اعتبارسنجی تاریخ
        @self.bot.message_handler(func=lambda message: self.user_status.get(message.chat.id) == 'waiting_for_date')
        def validate_date(message):
            order_date = message.text.strip()
            
            if re.match(self.date_pattern, order_date):
                self.bot.send_message(message.chat.id, 'لطفا نام و نام خانوادگی خود را به صورت کامل بنویسید')
                self.user_status[message.chat.id] = {'status': 'waiting_for_name', 'order_date': order_date}
            else:
                self.bot.send_message(message.chat.id, 'فرمت تاریخ نادرست است. لطفا تاریخ را به فرمت YYYY-MM-DD وارد کنید.')

        # هندلر برای دریافت نام و نام خانوادگی و جستجو در دیتابیس
        @self.bot.message_handler(func=lambda message: self.user_status.get(message.chat.id, {}).get('status') == 'waiting_for_name')
        def search_tracking_code(message: Message):
            order_date = self.user_status[message.chat.id]['order_date']
            full_name = message.text.strip()
            
            order = self.orders_collection.find_one({'full_name': full_name, 'order_date': order_date})
            
            if order:
                tracking_code = order.get('code')
                self.bot.send_message(message.chat.id, f'کد مرسوله شما: {tracking_code}')
            else:
                self.bot.send_message(message.chat.id, 'اطلاعاتی برای این سفارش یافت نشد.')
            
            self.user_status.pop(message.chat.id)
