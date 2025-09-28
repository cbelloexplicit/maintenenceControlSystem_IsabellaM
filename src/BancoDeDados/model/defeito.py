from datetime import date
from model.veiculo import Veiculo
from model.catalogo_defeito import CatalogoDefeito

class Defeito:
    def __init__(self, id_defeito:int, data_reporte:date, status_defeito:str, observacoes:str, veiculo:Veiculo = None, catalogo_defeito:CatalogoDefeito = None):
        self.__id_defeito = id_defeito
        self.__data_reporte = data_reporte
        self.__status_defeito = status_defeito
        self.__observacoes = observacoes
        self.__veiculo = veiculo
        self.__catalogo_defeito = catalogo_defeito

    # Getters
    def get_id_defeito(self) -> int:
        return self.__id_defeito

    def get_data_reporte(self) -> date:
        return self.__data_reporte

    def get_status_defeito(self) -> str:
        return self.__status_defeito

    def get_observacoes(self) -> str:
        return self.__observacoes

    def get_veiculo(self) -> Veiculo:
        return self.__veiculo

    def get_catalogo_defeito(self) -> CatalogoDefeito:
        return self.__catalogo_defeito

    # Setters
    def set_id_defeito(self, id_defeito:int):
        self.__id_defeito = id_defeito

    def set_data_reporte(self, data_reporte:date):
        self.__data_reporte = data_reporte

    def set_status_defeito(self, status_defeito:str):
        self.__status_defeito = status_defeito

    def set_observacoes(self, observacoes:str):
        self.__observacoes = observacoes

    def set_veiculo(self, veiculo:Veiculo):
        self.__veiculo = veiculo

    def set_catalogo_defeito(self, catalogo_defeito:CatalogoDefeito):
        self.__catalogo_defeito = catalogo_defeito

    # To String
    def to_string(self) -> str:
        veiculo_str = self.get_veiculo().get_placa() if self.get_veiculo() else "N/A"
        defeito_str = self.get_catalogo_defeito().get_descricao_defeito() if self.get_catalogo_defeito() else "N/A"
        return f"ID: {self.get_id_defeito()} | Veículo: {veiculo_str} | Defeito: {defeito_str} | Status: {self.get_status_defeito()}"