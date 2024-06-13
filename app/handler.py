from telegram import Update
from telegram.ext import ContextTypes


class Handler:
    def __init__(self, localization_dict):
        self.localization_dict = localization_dict
        self.step = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        self.step[user_id] = 'height'
        await update.message.reply_text("Hi, I am here to help you make life better!")
        await update.message.reply_text("Enter your height in cm")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        step = self.step.get(user_id, None)

        if step == 'height':
            height = update.message.text
            self.step[user_id] = 'weight'
            await update.message.reply_text("Enter your weight in kg")
            context.user_data['height'] = height
        elif step == 'weight':
            weight = update.message.text
            self.step[user_id] = 'user_id'
            await update.message.reply_text("Enter your user ID")
            context.user_data['weight'] = weight
        elif step == 'user_id':
            user_id = update.message.from_user.id
            height = context.user_data.get('height')
            weight = context.user_data.get('weight')
            await update.message.reply_text(f"Received data: Height - {height} cm, Weight - {weight} kg, User ID - {user_id}")
            self.step.pop(user_id, None)
