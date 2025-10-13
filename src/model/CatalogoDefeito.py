class CatalogoDefeito:
    def __init__(self, id_catalogo_defeito:int, codigo_defeito:str, descricao_defeito:str = None):
        self.__id_catalogo_defeito = id_catalogo_defeito
        self.__codigo_defeito = codigo_defeito
        self.__descricao_defeito = descricao_defeito

    # Getters
    def get_id_catalogo_defeito(self) -> int: 
        return self.__id_catalogo_defeito
    def get_codigo_defeito(self) -> str: 
        return self.__codigo_defeito
    def get_descricao_defeito(self) -> str: 
        return self.__descricao_defeito

    # Setters
    def set_id_catalogo_defeito(self, id_catalogo_defeito:int): 
        self.__id_catalogo_defeito = id_catalogo_defeito
    def set_codigo_defeito(self, codigo_defeito:str): 
        self.__codigo_defeito = codigo_defeito
    def set_descricao_defeito(self, descricao_defeito:str): 
        self.__descricao_defeito = descricao_defeito

    # To String
    def to_string(self) -> str:
        return f"[{self.get_codigo_defeito()}] {self.get_descricao_defeito()}"
