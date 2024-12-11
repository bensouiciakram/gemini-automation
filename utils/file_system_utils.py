from pathlib import Path 

class FileSystem :

    def __init__(self,input_path:str=None,output_path:str=None):
        self.input_path = Path(__file__).parents[1].joinpath('inputs') \
            if not input_path else Path(input_path)
        self.output_path = Path(__file__).parents[1].joinpath('outputs') \
            if not output_path else Path(output_path)

    def create_folders(self):
        self.input_path.mkdir(exist_ok=True)
        self.output_path.mkdir(exist_ok=True)
