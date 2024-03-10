from abc import ABC, abstractclassmethod
import json

class JsonFileImport(ABC):
    @abstractclassmethod
    def read_json_file(self): 
        pass



class JsonFileParameter(JsonFileImport):
    
    def __init__(self, json_file_path) -> None:
        self.json_file_path = json_file_path
        self.__json_data = None
        super().__init__()

    def read_json_file(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
            try:
                self.__json_data = json.load(json_file)
            except Exception as e:
                print(e)
                return 0
            finally:
                json_file.close()
        return 1
    
    @property
    def json_data(self):
        return self.__json_data
                

            


    
