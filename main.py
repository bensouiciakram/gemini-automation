import sys 
import json 
from pathlib import Path 
from utils.bot import GeminiBot
from utils.file_system_utils import FileSystem
from db.db_utils import Db 

# initialisations :
outputs_path = Path(__file__).parent.joinpath('outputs') # change it to be customizable
file_system = FileSystem(sys.argv[4],sys.argv[5])
database = Db('test.json')
bot = GeminiBot(
    executable=sys.argv[1],
    port=sys.argv[2],
    overloading_export=sys.argv[3] if len(sys.argv) > 3 else 0
)

def new_file_handler(input_file:str):
    database.add_config(input_file)
    bot.export(
        bot.search(input_file),
        outputs_path,
        input_file
    )
    # TODO 4 : fire event file used 

def handle_file_used(input_file:str):
    database.set_used(input_file)

if __name__ == '__main__':
    new_inputs = file_system.check_new_input_files(
        database.check_non_existance
    )
    new_file_handler('./inputs/2001.json')
    breakpoint()
    # bot.export(bot.search())
