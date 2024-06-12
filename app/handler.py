import asyncio
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import (ContextTypes)
import time

class Handler:
    def __init__(self, localization_dict: dict, default_localization='en'):
        self.default_localization = default_localization
        self.localization_dict = localization_dict

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi, i am help you to make life better!")

        await self.enter_data(update, context)

    async def enter_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # await update.message.reply_text("Enter your height in cm")

        # height_msg = update.message.from_user

        # await update.message.reply_text("Enter your weight in kg")

        # weight_msg = update.message.from_user

        # await update.message.reply_text("Enter your user ID")

        # user_id_msg = update.message.from_user.id

        # await update.message.reply_text(f"Height: {height_msg}\nWeight: {weight_msg}\nUser ID: {user_id_msg}")