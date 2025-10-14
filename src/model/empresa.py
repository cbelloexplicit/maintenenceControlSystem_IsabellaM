class Empresa:
    def __init__(self, id_empresa:int, nome_fantasia:str, endereco:str):
        self.__id_empresa = id_empresa
        self.__nome_fantasia = nome_fantasia
        self.__endereco = endereco

    # Getters
    def get_id_empresa(self) -> int: 
        return self.__id_empresa
    def get_nome_fantasia(self) -> str: 
        return self.__nome_fantasia
    def get_endereco(self) -> str: 
        return self.__endereco

    # Setters
    def set_id_empresa(self, id_empresa:int): 
        self.__id_empresa = id_empresa
    def set_nome_fantasia(self, nome_fantasia:str): 
        self.__nome_fantasia = nome_fantasia
    def set_endereco(self, endereco:str): 
        self.__endereco = endereco

    # To String
    def to_string(self) -> str:
        return f"ID: {self.get_id_empresa()} | Nome Fantasia: {self.get_nome_fantasia()}"
