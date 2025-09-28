class Tecnico:
    def __init__(self, id_tecnico:int, nome_tecnico:str):
        self.__id_tecnico = id_tecnico
        self.__nome_tecnico = nome_tecnico

    # Getters
    def get_id_tecnico(self) -> int:
        return self.__id_tecnico

    def get_nome_tecnico(self) -> str:
        return self.__nome_tecnico

    # Setters
    def set_id_tecnico(self, id_tecnico:int):
        self.__id_tecnico = id_tecnico

    def set_nome_tecnico(self, nome_tecnico:str):
        self.__nome_tecnico = nome_tecnico

    # To String
    def to_string(self) -> str:
        return f"ID: {self.get_id_tecnico()} | Nome: {self.get_nome_tecnico()}"