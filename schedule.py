import telebot
import logging
from config import TOKEN
from data import teachers_data, schedule_data, start_txt, help_txt


class ScheduleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.logger = logging.getLogger(__name__)
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков сообщений"""
        self.bot.message_handler(commands=['start'])(self.handle_start)
        self.bot.message_handler(commands=['help'])(self.handle_help)
        self.bot.message_handler(commands=['teachers'])(self.handle_teachers)
        self.bot.message_handler(func=lambda message: True)(self.handle_text)

    def handle_start(self, message):
        self.bot.send_message(message.chat.id, start_txt)

    def handle_help(self, message):
        self.bot.send_message(message.chat.id, help_txt)

    def handle_teachers(self, message):
        if teachers_data:
            teachers_info = "\n".join([
                f"{subject}: {', '.join(teachers)}"
                for subject, teachers in teachers_data.items()
            ])
            self.bot.send_message(
                message.chat.id,
                f"Список преподавателей:\n{teachers_info}"
            )
        else:
            self.bot.send_message(
                message.chat.id,
                "Список преподавателей пуст."
            )

    def handle_text(self, message):
        text = message.text.lower()

        if "скинь расписание" in text or "cкинь расписание" in text:
            day = None
            week_type = None

            if "понедельник" in text:
                day = 'понедельник'
            elif "вторник" in text:
                day = 'вторник'
            elif "среду" in text:
                day = 'среду'
            elif "четверг" in text:
                day = 'четверг'
            elif "пятницу" in text:
                day = 'пятницу'
            elif "субботу" in text:
                day = 'субботу'
            elif "воскресенье" in text:
                day = 'воскресенье'

            if "по 1 неделе" in text or "по нечётной неделе" in text or "по нечетной неделе" in text:
                week_type = '1'
            elif "по 2 неделе" in text or "по чётной неделе" in text or "по четной неделе" in text:
                week_type = '2'

            if day and week_type:
                schedule = schedule_data.get(day, {}).get(week_type, "Извините, расписание не найдено.")
                self.bot.send_message(message.chat.id, schedule)
            else:
                self.bot.send_message(message.chat.id, 'Пожалуйста, уточните день недели и тип недели.')
        else:
            self.bot.send_message(
                message.chat.id,
                'Я не понимаю ваш запрос.\n\n'
                'Попробуйте спросить о расписании или введите команду /teachers для получения списка преподавателей.\n\n'
                'Используйте команду /help чтобы ознакомиться с моим функционалом.'
            )


# Инициализация бота
bot_instance = ScheduleBot()
bot = bot_instance.bot  # Для обратной совместимости с текущим Bot.py

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
