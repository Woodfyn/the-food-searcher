from configs.config import Config
from app.bot import Bot
from app.handler import Handler
from app.mongo import Mongo
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

logging.basicConfig(filename='bot.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    cfg = Config()

    client = MongoClient(cfg.mongo_uri, server_api=ServerApi('1'))

    bot = Bot(Handler(cfg.localization_dict, Mongo(client)), cfg.bot_token)

    logger.info('Bot started...')
    bot.run()

if __name__ == '__main__':
    main()
