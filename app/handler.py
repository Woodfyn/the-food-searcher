from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    CallbackQuery,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters
)    
from .utils import calculate_plan
from .mongo import Mongo

INPUT_PLAN = '1'
CALCULATE_PLAN = '2'

MENU_ADD_FOOD = '1'
MENU_UPDATE_DATA = '2'

class Handler:
    def __init__(self, localization_dict: dict, mongo: Mongo, default_localization='en'):
        self.default_localization = default_localization
        self.localization_dict = localization_dict
        self.step = {}
        self.mongo = mongo
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id

        user_data = await self.mongo.get_user_by_id(user_id)

        if user_data:
            await update.message.reply_text(f"Welcome back! I see you have already provided your details.")
            await self.menu(update, context)
        else:
            self.step[user_id] = 'height'
            await update.message.reply_text("Hi, I am here to help you make life better!")
            await update.message.reply_text("Enter your height in cm.\nExample ➜ Height: 184.0 or 165.6")

    async def _update_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id

        try:
            self.mongo.delete_user_by_id(user_id)

            self.step[user_id] = 'height'
            await update.message.reply_text("Enter your height in cm.\nExample ➜ Height: 184.0 or 165.6")

            await self.handle_message(update, context)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        current_step = self.step.get(user_id, None)

        if current_step:
            if current_step == 'height':
                await self._handle_height(update, context)
            elif current_step == 'weight':
                await self._handle_weight(update, context)
            elif current_step == 'age':
                await self._handle_age(update, context)
            elif current_step == 'sex':
                await self._handle_sex(update, context)
            elif current_step == 'input_plan_response':
                await self._handle_input_plan_response(update, context)
            
    async def _handle_height(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        height = update.message.text

        try:
            height_float = float(height)
            if 40.0 <= height_float <= 250.0:
                context.user_data['height'] = height_float
                self.step[user_id] = 'weight'
                await update.message.reply_text("Enter your weight in kg\nExample ➜ Weight: 80.0 or 84.2")
            else:
                await update.message.reply_text("Please enter a valid height in cm (between 40 and 250)")
        except ValueError:
            await update.message.reply_text("Please enter a valid height in cm")

    async def _handle_weight(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        weight = update.message.text

        try:
            weight_float = float(weight)
            if 4.0 <= weight_float <= 560.0:
                context.user_data['weight'] = weight_float
                self.step[user_id] = 'age'
                await update.message.reply_text("Enter your age in years\nExample ➜ Age: 30.1 or 25.6")
            else:
                await update.message.reply_text("Please enter a valid weight in kg (between 4 and 560)")
        except ValueError:
            await update.message.reply_text("Please enter a valid weight in kg")

    async def _handle_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        age = update.message.text

        try:
            age_float = float(age)
            if 0.0 <= age_float <= 120.0:
                context.user_data['age'] = age_float
                self.step[user_id] = 'sex'
                await update.message.reply_text("Enter your sex.\nExample ➜ Male or Female")
            else:
                await update.message.reply_text("Please enter a valid age in years (between 0 and 120)")
        except ValueError:
            await update.message.reply_text("Please enter a valid age in years")

    async def _handle_sex(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        sex = update.message.text.strip().capitalize()

        if sex in ['Male', 'Female']:
            context.user_data['sex'] = sex.lower()
            self.step[user_id] = 'factor'

            buttons = [
                [InlineKeyboardButton('1', callback_data='1.2')],
                [InlineKeyboardButton('2', callback_data='1.375')],
                [InlineKeyboardButton('3', callback_data='1.55')],
                [InlineKeyboardButton('4', callback_data='1.725')],
                [InlineKeyboardButton('5', callback_data='1.9')]
            ]

            reply_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                'Now you need to enter your activity coefficient: \n'
                '1. If you have no physical activity and have a sedentary job, multiply the result by 1.2\n'
                '2. If you do a little jogging or light gymnastics 1-3 times a week, multiply the calories by 1.375\n'
                '3. If you exercise moderately 3-5 times a week, multiply the calories by 1.55\n'
                '4. If you work out fully 6-7 times a week, multiply the result by 1.725\n'
                '5. And finally, if your job is related to physical labor, you train 2 times a day and include strength exercises in your training program, your coefficient will be equal to 1.9',
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text('Please enter "Male" or "Female"')

    async def handle_factor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        factor = query.data

        context.user_data['factor'] = float(factor)
        await query.edit_message_text(text=f"Your activity coefficient is set to {factor}.")

        buttons = [
            [InlineKeyboardButton('You can enter your calorie intake', callback_data=INPUT_PLAN)],
            [InlineKeyboardButton('Or I suggest that you let me calculate your calorie intake for you', callback_data=CALCULATE_PLAN)]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_text(
            'What do you want to do next?',
            reply_markup=reply_markup
        )

    async def handle_plan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        choose = query.data

        if choose == INPUT_PLAN:
            self.step[user_id] = 'input_plan_response'
            await query.edit_message_text("Please enter your desired daily calorie intake.\nExample ➜ 2000.0 or 1234.5")
        elif choose == CALCULATE_PLAN:
            await query.edit_message_text("Calculating your plan...")   
            await self._save_user_data_and_calculate_plan(query, context)

    async def _handle_input_plan_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        plan = update.message.text

        try:
            plan_float = float(plan)
            context.user_data['plan'] = plan_float

            await self._save_user_data_and_notify(update, context)

            self.step.pop(user_id)
        except ValueError:
            await update.message.reply_text("Please enter a valid number for your daily calorie intake.")

    async def _save_user_data_and_calculate_plan(self, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
        user_id = query.from_user.id
        height = context.user_data.get('height', 'not provided')
        weight = context.user_data.get('weight', 'not provided')
        age = context.user_data.get('age', 'not provided')
        sex = context.user_data.get('sex', 'not provided')
        factor = context.user_data.get('factor', 'not provided')
        plan = calculate_plan(height, weight, age, sex, factor)

        try:
            await self.mongo.create_user(user_id, height, weight, age, sex, factor, plan)
            await query.message.reply_text(f'Your calculated plan is: {plan}\nNow go to the menu: write /menu')
        except Exception as e:
            await query.message.reply_text(f"Error storing user data: {e}")

    async def _save_user_data_and_notify(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        height = context.user_data.get('height', 'not provided')
        weight = context.user_data.get('weight', 'not provided')
        age = context.user_data.get('age', 'not provided')
        sex = context.user_data.get('sex', 'not provided')
        factor = context.user_data.get('factor', 'not provided')
        plan = context.user_data.get('plan', 'not provided')

        try:
            await self.mongo.create_user(user_id, height, weight, age, sex, factor, plan)
            await update.message.reply_text(f'Your daily calorie intake has been set to: {plan}\nNow go to the menu: write /menu')
        except Exception as e:
            await update.message.reply_text(f'Error storing user data: {e}')

    async def menu(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        user_data = await self.mongo.get_user_by_id(user_id)

        if user_data:
            buttons = [
                [InlineKeyboardButton('Add food', callback_data=MENU_ADD_FOOD)],
                [InlineKeyboardButton('Update data', callback_data=MENU_UPDATE_DATA)],
            ]

            reply_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                'What do you want to do?',
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text('Please start the bot!')

    async def button_callback(self, update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        choose = query.data

        if choose == MENU_ADD_FOOD:
            await query.edit_message_text("Please enter your food name.\nExample ➜ Apple")
            self._add_food(update, context)

        elif choose == MENU_UPDATE_DATA:
            await query.edit_message_text("Updating your data...")
            await self._update_data(update, context)

        

    async def _add_food(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Sent food name: ' + update.message.text)
