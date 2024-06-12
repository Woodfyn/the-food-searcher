import telebot
from telebot import types

class Handler:
    def __init__(self, bot: telebot.TeleBot, localization: dict, default_language='en'):
        self.bot = bot
        self.user_language = {}
        self.default_language = default_language
        self.localization = localization

    def localized_text(self, key: str, language: str) -> str:
        return self.localization.get(language, {}).get(key, key)

    def start(self, message):
        language = self.user_language.get(message.from_user.id, self.default_language)
        self.bot.send_message(message.chat.id, self.localized_text('start_message', language))

    def help(self, message):
        language = self.user_language.get(message.from_user.id, self.default_language)
        self.bot.send_message(message.chat.id, self.localized_text('help_message', language))

    def reset(self, message):
        language = self.user_language.get(message.from_user.id, self.default_language)
        self.bot.send_message(message.chat.id, self.localized_text('reset_message', language))

    def resend(self, message):
        language = self.user_language.get(message.from_user.id, self.default_language)
        self.bot.send_message(message.chat.id, self.localized_text('resend_message', language))

    def set_language(self, message):
        self.bot.send_message(message.chat.id, self.localized_text('choose_language', self.default_language))
        self.bot.register_next_step_handler(message, self.choose_language_step)

    def choose_language_step(self, message):
        match message.text:
            case '/en':
                self.user_language[message.from_user.id] = 'en'
                self.bot.send_message(message.chat.id, self.localized_text('language_set', 'en'))
            case '/uk':
                self.user_language[message.from_user.id] = 'uk'
                self.bot.send_message(message.chat.id, self.localized_text('language_set', 'uk'))
            case _:
                self.bot.send_message(message.chat.id, "Invalid language. Please choose again.")
                self.set_language(message)