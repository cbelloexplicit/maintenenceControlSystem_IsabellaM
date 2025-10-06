from datetime import date

class Lote:
    def __init__(self, id_lote:int, codigo_lote:str, descricao:str, data_compra:date):
        self.__id_lote = id_lote
        self.__codigo_lote = codigo_lote
        self.__descricao = descricao
        self.__data_compra = data_compra

    # Getters
    def get_id_lote(self) -> int:
        return self.__id_lote

    def get_codigo_lote(self) -> str:
        return self.__codigo_lote

    def get_descricao(self) -> str:
        return self.__descricao

    def get_data_compra(self) -> date:
        return self.__data_compra

    # Setters
    def set_id_lote(self, id_lote:int):
        self.__id_lote = id_lote

    def set_codigo_lote(self, codigo_lote:str):
        self.__codigo_lote = codigo_lote

    def set_descricao(self, descricao:str):
        self.__descricao = descricao

    def set_data_compra(self, data_compra:date):
        self.__data_compra = data_compra

    # To String
    def to_string(self) -> str:
        return f"ID: {self.get_id_lote()} | Código: {self.get_codigo_lote()} | Descrição: {self.get_descricao()}"
