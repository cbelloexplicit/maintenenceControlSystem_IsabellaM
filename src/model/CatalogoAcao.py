class CatalogoAcao:
    def __init__(self, id_catalogo_acao:int, codigo_acao:str, descricao_acao:str = None):
        self.__id_catalogo_acao = id_catalogo_acao
        self.__codigo_acao = codigo_acao
        self.__descricao_acao = descricao_acao

    # Getters
    def get_id_catalogo_acao(self) -> int: 
        return self.__id_catalogo_acao
    def get_codigo_acao(self) -> str: 
        return self.__codigo_acao
    def get_descricao_acao(self) -> str: 
        return self.__descricao_acao

    # Setters
    def set_id_catalogo_acao(self, id_catalogo_acao:int): 
        self.__id_catalogo_acao = id_catalogo_acao
    def set_codigo_acao(self, codigo_acao:str): 
        self.__codigo_acao = codigo_acao
    def set_descricao_acao(self, descricao_acao:str): 
        self.__descricao_acao = descricao_acao

    # To String
    def to_string(self) -> str:
        return f"[{self.get_codigo_acao()}] {self.get_descricao_acao()}"
