from configs.config import Config
from app.bot import Bot
from app.handler import Handler
import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    cfg = Config()
    handler = Handler(cfg.localization_dict)
    bot = Bot(handler, cfg.bot_token)

    logger.info('Bot started...')
    bot.run()


if __name__ == '__main__':
    main()
