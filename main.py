import sys 
from utils.bot import GeminiBot
from utils.file_system_utils import create_folders


if __name__ == '__main__':
    create_folders(sys.argv[4],sys.argv[5])
    bot = GeminiBot(
        executable=sys.argv[1],
        port=sys.argv[2],
        overloading_export=sys.argv[3] if len(sys.argv) > 3 else 0
    )
    breakpoint()
    bot.export(bot.search())
