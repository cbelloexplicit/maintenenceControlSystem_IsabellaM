from datetime import date
from model.tecnico import Tecnico

class VisitaTecnica:
    def __init__(self, id_visita:int, data_visita:date, tecnico:Tecnico = None):
        self.__id_visita = id_visita
        self.__data_visita = data_visita
        self.__tecnico = tecnico

    # Getters
    def get_id_visita(self) -> int:
        return self.__id_visita

    def get_data_visita(self) -> date:
        return self.__data_visita

    def get_tecnico(self) -> Tecnico:
        return self.__tecnico

    # Setters
    def set_id_visita(self, id_visita:int):
        self.__id_visita = id_visita

    def set_data_visita(self, data_visita:date):
        self.__data_visita = data_visita

    def set_tecnico(self, tecnico:Tecnico):
        self.__tecnico = tecnico

    # To String
    def to_string(self) -> str:
        tecnico_str = self.get_tecnico().get_nome_tecnico() if self.get_tecnico() else "N/A"
        return f"ID Visita: {self.get_id_visita()} | Data: {self.get_data_visita()} | Técnico: {tecnico_str}"