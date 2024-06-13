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
        await update.message.reply_text("Enter your height in cm (whole number)")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        step = self.step.get(user_id, None)

        if step == 'height':
            height = update.message.text
            if height.isdigit() and 40 <= int(height) <= 250:
                context.user_data['height'] = height
                self.step[user_id] = 'weight'
                await update.message.reply_text("Enter your weight in kg (whole number)")
            else:
                await update.message.reply_text("Enter your height in cm correctly")

        elif step == 'weight':
            weight = update.message.text
            if weight.isdigit() and 4 <= int(weight) <= 560:
                context.user_data['weight'] = weight

                height = context.user_data.get('height', 'not provided')
                weight = context.user_data.get('weight', 'not provided')

                await update.message.reply_text(f"Received data: Height - {height} cm, Weight - {weight} kg, User ID - {user_id}")

                self.step.pop(user_id, None)
            else:
                await update.message.reply_text("Enter your weight in kg correctly")
