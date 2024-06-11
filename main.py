from configs.config import Config
from bots.bot import Bot

def main():
    cfg = Config()

    bot = Bot(cfg.bot_token)

    print("Started!")
    bot.run()

if __name__ == '__main__':
    main()