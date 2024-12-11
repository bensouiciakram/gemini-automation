from pathlib import Path 
from typing import Callable,List

class FileSystem :

    def __init__(self,input_path:str=None,output_path:str=None):
        self.input_path = Path(__file__).parents[1].joinpath('inputs') \
            if not input_path else Path(input_path)
        self.output_path = Path(__file__).parents[1].joinpath('outputs') \
            if not output_path else Path(output_path)
        self.create_folders()

    def create_folders(self):
        self.input_path.mkdir(exist_ok=True)
        self.output_path.mkdir(exist_ok=True)

    def check_new_input_files(self,checker:Callable) -> List[str]:
        input_files = [file.name for file in self.input_path.iterdir() if file.is_file()]
        new_inputs = [input_file for input_file in input_files if checker(input_file)]
        new_inputs.sort()
        return new_inputs
