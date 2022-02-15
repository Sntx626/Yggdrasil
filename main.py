import os

from src.bot import get_bot

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot = get_bot()
    bot.run()
