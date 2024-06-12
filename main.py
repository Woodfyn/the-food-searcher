from configs.config import Config
from bots.bot import Bot
import logging

logger = logging.basicConfig(filename='bot.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    cfg = Config()

    bot = Bot(cfg.bot_token, cfg.localization_dict)

    logger.info('Bot started...')
    bot.run()

if __name__ == '__main__':
    main()
