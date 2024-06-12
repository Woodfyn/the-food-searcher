import telebot
from telebot import types
from .handlers import Handler

class Bot:
    def __init__(self, token, localization: dict):
        self.bot = telebot.TeleBot(token)
        self.handler = Handler(self.bot, localization)
        self.commands_list = [
            types.BotCommand(command='help', description='Show help information'),
            types.BotCommand(command='reset', description='Reset the bot'),
            types.BotCommand(command='resend', description='Resend the last message'),
            types.BotCommand(command='set_language', description='Set your preferred language')
        ]
        self.bot.set_my_commands(self.commands_list)

        self.bot.message_handler(commands=['start'])(self.handler.start)
        self.bot.message_handler(commands=['help'])(self.handler.help)
        self.bot.message_handler(commands=['reset'])(self.handler.reset)
        self.bot.message_handler(commands=['resend'])(self.handler.resend)
        self.bot.message_handler(commands=['set_language'])(self.handler.set_language)

    def run(self):
        self.bot.polling()
