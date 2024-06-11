import telebot
from telebot import types

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    @self.bot.message_handler(commands=['start'])
    def start(self, message):
        self.bot.send_message(message.chat.id, "Hi, I'm a bot. Type /help for more info.")

    def run(self):
        self.bot.polling()