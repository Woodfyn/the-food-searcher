import telebot
from telebot import types


class Bot:

    def __init__(self, token, default_language='en'):

        self.bot = telebot.TeleBot(token)
        self.default_language = default_language
        self.user_language = {}
        self.commands = [
            types.BotCommand(
                command='help', description='Show help information'),
            types.BotCommand(command='reset', description='Reset the bot'),
            types.BotCommand(command='resend',
                             description='Resend the last message'),
            types.BotCommand(command='set_language',
                             description='Set your preferred language')
        ]
        self.bot.set_my_commands(self.commands)
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['reset'])(self.reset)
        self.bot.message_handler(commands=['resend'])(self.resend)
        self.bot.message_handler(commands=['set_language'])(self.set_language)

    def localized_text(self, key: str, language: str) -> str:

        localization_dict = {
            'help_description': {
                'en': 'Show help information',
                'uk': 'Показати інформацію допомоги'
            },
            'reset_description': {
                'en': 'Reset the bot',
                'uk': 'Скинути бота'
            },
            'resend_description': {
                'en': 'Resend the last message',
                'uk': 'Повторно надіслати останнє повідомлення'
            },
            'start_message': {
                'en': "Hi, I'm a bot. Type /help for more info.",
                'uk': "Привіт, я бот. Напишіть /help для отримання додаткової інформації."
            },
            'help_message': {
                'en': "Here are the available commands:\n/help - Show help information\n/reset - Reset the bot\n/resend - Resend the last message\n/set_language - Set your preferred language",
                'uk': "Ось доступні команди:\n/help - Показати інформацію допомоги\n/reset - Скинути бота\n/resend - Повторно надіслати останнє повідомлення\n/set_language - Встановити бажану мову"
            },
            'reset_message': {
                'en': "Bot has been reset.",
                'uk': "Бот був скинутий."
            },
            'resend_message': {
                'en': "Last message has been resent.",
                'uk': "Останнє повідомлення було повторно надіслано."
            },
            'choose_language': {
                'en': "Please choose your language:\n/en - English\n/uk - Українська",
                'uk': "Будь ласка, оберіть свою мову:\n/en - English\n/uk - Українська"
            },
            'language_set': {
                'en': "Language has been set to English.",
                'uk': "Мова була встановлена на українську."
            }
        }
        return localization_dict[key].get(language, key)

    def start(self, message):
        language = self.user_language.get(
            message.from_user.id, self.default_language)
        self.bot.send_message(
            message.chat.id, self.localized_text('start_message', language))

    def help(self, message):
        language = self.user_language.get(
            message.from_user.id, self.default_language)
        self.bot.send_message(
            message.chat.id, self.localized_text('help_message', language))

    def reset(self, message):
        language = self.user_language.get(
            message.from_user.id, self.default_language)
        self.bot.send_message(
            message.chat.id, self.localized_text('reset_message', language))

    def resend(self, message):
        language = self.user_language.get(
            message.from_user.id, self.default_language)
        self.bot.send_message(
            message.chat.id, self.localized_text('resend_message', language))

    def set_language(self, message):
        self.bot.send_message(
            message.chat.id, self.localized_text('choose_language', self.default_language))
        self.bot.register_next_step_handler(message, self.choose_language_step)

    def choose_language_step(self, message):
        if message.text == '/en':
            self.user_language[message.from_user.id] = 'en'
            self.bot.send_message(
                message.chat.id, self.localized_text('language_set', 'en'))
        elif message.text == '/uk':
            self.user_language[message.from_user.id] = 'uk'
            self.bot.send_message(
                message.chat.id, self.localized_text('language_set', 'uk'))
        else:
            self.bot.send_message(
                message.chat.id, "Invalid language. Please choose again.")
            self.set_language(message)

    def run(self):
        self.bot.polling()
