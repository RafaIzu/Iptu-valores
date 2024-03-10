class Parameters():
    def __init__(self, json_data) -> None:
        self.__main_url = json_data['main_url']
        self.__driver = json_data['driver']
        self.__db_user = json_data['db_user']
        self.__db_pw =  json_data['db_pw']
        self.__db_server = json_data['db_server']
        self.__db_port =  json_data['db_port']
        self.__db_name = json_data['db_name']
    
    @property
    def main_url(self):
        return self.__main_url
    
    @property
    def driver(self):
        return self.__driver
    
    @property
    def db_user(self):
        return self.__db_user
    
    @property
    def db_pw(self):
        return self.__db_pw
    
    @property
    def db_server(self):
        return self.__db_server
    
    @property
    def db_port(self):
        return self.__db_port
    
    @property
    def db_name(self):
        return self.__db_name
    
