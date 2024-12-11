from pathlib import Path 

def create_folders(input_path:str,output_path:str):
    input_path = Path(__file__).parents[1].joinpath('inputs') \
        if not input_path else Path(input_path)
    output_path = Path(__file__).parents[1].joinpath('outputs') \
        if not output_path else Path(output_path)
    input_path.mkdir(exist_ok=True)
    output_path.mkdir(exist_ok=True)
