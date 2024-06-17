import os
from dotenv import load_dotenv
import json

class Config:
    def __init__(self):
        load_dotenv()

        self.bot_token = os.getenv('BOT_TOKEN')
        if self.bot_token is None:
            raise ValueError('BOT_TOKEN is not set')
        
        with open('localization.json', 'r', encoding='utf-8') as f:
            self.localization_dict = json.load(f)
        
        self.mongo_uri = os.getenv('MONGO_URI')

    def __str__(self):
        return f"Config(bot_token={self.bot_token}, localization_dict={self.localization_dict})"
