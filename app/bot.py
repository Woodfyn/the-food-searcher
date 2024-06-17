from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder, Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters
)
from .handler import (
    Handler, INPUT_PLAN, CALCULATE_PLAN
)

class Bot:
    def __init__(self, handler: Handler, token: str):
        self.handler = handler
        self.token = token
        self.commands = [
            BotCommand(command='start', description='Start bot'),
            BotCommand(command='menu', description='Go to menu'),
        ]

    async def post_init(self, application: Application) -> None:
        await application.bot.set_my_commands(self.commands)

    def run(self):
        application = ApplicationBuilder() \
            .token(self.token) \
            .post_init(self.post_init) \
            .build()

        application.add_handler(CommandHandler('start', self.handler.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.handle_message))
        application.add_handler(CallbackQueryHandler(self.handler.handle_factor, pattern='^1\.2|1\.375|1\.55|1\.725|1\.9$'))
        application.add_handler(CallbackQueryHandler(self.handler.handle_plan))
        application.add_handler(CommandHandler('menu', self.handler.menu))

        application.run_polling()