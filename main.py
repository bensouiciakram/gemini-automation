import sys 
from utils.bot import GeminiBot

if __name__ == '__main__':
    bot = GeminiBot(
        executable=sys.argv[1],
        port=sys.argv[2],
        overloading_export=sys.argv[3] if len(sys.argv) > 3 else 0
    )
    bot.export(bot.search())
