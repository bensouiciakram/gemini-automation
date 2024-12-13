import sys 
import json 
from pathlib import Path 
from time import sleep 
from pyee.base import EventEmitter 
from utils.bot import GeminiBot
from utils.file_system_utils import FileSystem
from utils.exceptions import CloseWindowException
from db.db_utils import Db 

# initialisations :
event_emitter = EventEmitter()
outputs_path = Path(__file__).parent.joinpath('outputs')
inputs_path = Path(__file__).parent.joinpath('inputs')
file_system = FileSystem(sys.argv[4],sys.argv[5])
database = Db('db.json')
bot = GeminiBot(
    executable=sys.argv[1],
    port=sys.argv[2],
    overloading_export=sys.argv[3] if len(sys.argv) > 3 else 0
)


@event_emitter.on('new_file')
def new_file_handler(input_file:str):
    database.add_config(Path(input_file).name)
    bot.export(
        bot.search(input_file),
        outputs_path,
        input_file
    )
    event_emitter.emit(
        'file_used',
        str(inputs_path.joinpath(input_file).absolute())
    )
    bot.check_close_window(input_file)

@event_emitter.on('file_used')
def handle_file_used(input_file:str):
    database.set_used(Path(input_file).name)

if __name__ == '__main__':
    while True :
        new_inputs = file_system.check_new_input_files(
            database.check_non_existance_or_not_used
        )
        try :
            if new_inputs :
                print('New Files found')
                [
                    event_emitter.emit('new_file',str(inputs_path.joinpath(input_path).absolute())) 
                    for  input_path in new_inputs
                ]
            else :
                print('No new files...')

            print('Sleeping for 3 seconds')
            sleep(3)
        except CloseWindowException :
            print('closing prompt have been found')
            break  
    # bot.free_up_playwright_resources()
    # bot.export(bot.search())
