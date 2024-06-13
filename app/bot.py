from telegram import BotCommand
from telegram.ext import ApplicationBuilder, Application, CommandHandler, MessageHandler, filters
from .handler import Handler


class Bot:
    def __init__(self, handler: Handler, token: str):
        self.handler = handler
        self.token = token
        self.handler_list = [
            BotCommand(command='start', description='Start bot'),
        ]

    async def post_init(self, application: Application) -> None:
        await application.bot.set_my_commands(self.handler_list)

    def run(self):
        application = ApplicationBuilder() \
            .token(self.token) \
            .post_init(self.post_init) \
            .build()

        application.add_handler(CommandHandler('start', self.handler.start))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handler.handle_message))
        application.run_polling()
