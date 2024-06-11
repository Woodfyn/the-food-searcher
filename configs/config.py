import os
from dotenv import load_dotenv

import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.bot_token = os.getenv('BOT_TOKEN')
        self.default_language = os.getenv('DEFAULT_LANGUAGE', 'en')

        if self.bot_token is None:
            raise ValueError('BOT_TOKEN is not set')

    def __str__(self):
        return f"Config(bot_token={self.bot_token}, default_language={self.default_language})"
