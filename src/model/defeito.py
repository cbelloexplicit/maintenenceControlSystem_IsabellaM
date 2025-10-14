from datetime import date
from src.model.catalogo_defeito import CatalogoDefeitos
from src.model.veiculo import Veiculo

class Defeito:
    def __init__(self, id_defeito:int, data_reporte:date, status_defeito:str, obs_defeitos:str, catalogo_defeito:CatalogoDefeito, veiculo:Veiculo):
        self.__id_defeito = id_defeito
        self.__data_reporte = data_reporte
        self.__status_defeito = status_defeito
        self.__obs_defeitos = obs_defeitos
        self.__catalogo_defeito = catalogo_defeito
        self.__veiculo = veiculo

    # Getters
    def get_id_defeito(self) -> int: 
        return self.__id_defeito
    def get_data_reporte(self) -> date: 
        return self.__data_reporte
    def get_status_defeito(self) -> str: 
        return self.__status_defeito
    def get_obs_defeitos(self) -> str: 
        return self.__obs_defeitos
    def get_catalogo_defeito(self) -> CatalogoDefeitos:
        return self.__catalogo_defeito
    def get_veiculo(self) -> Veiculo: 
        return self.__veiculo

    # Setters
    def set_id_defeito(self, id_defeito:int): 
        self.__id_defeito = id_defeito
    def set_data_reporte(self, data_reporte:date): 
        self.__data_reporte = data_reporte
    def set_status_defeito(self, status_defeito:str): 
        self.__status_defeito = status_defeito
    def set_obs_defeitos(self, obs_defeitos:str): 
        self.__obs_defeitos = obs_defeitos
    def set_catalogo_defeito(self, catalogo_defeito:CatalogoDefeitos):
        self.__catalogo_defeito = catalogo_defeito
    def set_veiculo(self, veiculo:Veiculo): 
        self.__veiculo = veiculo

    # To String
    def to_string(self) -> str:
        placa = self.get_veiculo().get_placa() if self.get_veiculo() else "N/A"
        return f"ID: {self.get_id_defeito()} | Status: {self.get_status_defeito()} | Veículo: {placa}"
