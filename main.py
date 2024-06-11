import telebot as tg
from configs.config import Config

def main():
    cfg = Config()

    bot = tg.TeleBot(cfg.bot_token)

if __name__ == '__main__':
    main()