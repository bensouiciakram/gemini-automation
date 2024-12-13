from typing import List 
from tinydb import TinyDB,Query

class Db :
    def __init__(self,db_name:str):
        self.db_name = db_name 
        self.db = TinyDB(self.db_name)
        self.Config = Query()

    def add_config(self,input_path:str,used:bool=False):
        self.db.insert(
            {
                'input_path':input_path,
                'used':used 
            }
        )

    def set_used(self,file_path:str):
        self.db.update(
            {'used':True},
            self.Config.input_path == file_path
        )

    def check_non_existance_or_not_used(self,file_path:str) -> bool :
        db_file_obj = self.db.search(self.Config.input_path == file_path)
        if not db_file_obj :
            return True 
        elif not db_file_obj[0]['used']:
            return True 
        else :
            return False
    
    def search_unused(self) -> List[dict]:
        return self.db.search(self.Config.used == False)
        