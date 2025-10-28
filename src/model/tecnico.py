from src.model.contato import Contato

class Tecnico:
    def __init__(self, id_tecnico:int, local:str, status:str, contato:Contato):
        self.__id_tecnico = id_tecnico
        self.__status = status
        self.__local = local
        self.__contato = contato

    def get_status(self) -> str:
        return self.__status
    def get_id_tecnico(self) -> int: 
        return self.__id_tecnico
    def get_local(self) -> str: 
        return self.__local
    def get_contato(self) -> Contato: 
        return self.__contato

    def set_status(self, status: str) -> None:
        self.__status = status
    def set_id_tecnico(self, id_tecnico:int): 
        self.__id_tecnico = id_tecnico
    def set_local(self, local:str): 
        self.__local = local
    def set_contato(self, contato:Contato): 
        self.__contato = contato

    def to_string(self) -> str:
        nome = self.get_contato().get_nome_contato() if self.get_contato() else "N/A"
        return f"TÉCNICO -> ID: {self.get_id_tecnico()} | Nome: {nome} | Local: {self.get_local()} | Contato: {self.get_contato()} | Status: {self.get_status()}"
