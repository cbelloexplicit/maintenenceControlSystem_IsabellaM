from datetime import datetime
from model.lote import Lote
from model.veiculo import Veiculo
from model.empresa import Empresa
from model.manutencao import Manutencao

class LogLote:
    def __init__(self, id_log:int, data_evento:datetime, tipo_evento:str, observacao:str, 
                 lote:Lote, veiculo:Veiculo = None, empresa:Empresa = None, manutencao:Manutencao = None):
        self.__id_log = id_log
        self.__data_evento = data_evento
        self.__tipo_evento = tipo_evento
        self.__observacao = observacao
        self.__lote = lote
        self.__veiculo = veiculo
        self.__empresa = empresa
        self.__manutencao = manutencao

    # Getters
    def get_id_log(self) -> int:
        return self.__id_log

    def get_data_evento(self) -> datetime:
        return self.__data_evento

    def get_tipo_evento(self) -> str:
        return self.__tipo_evento

    def get_observacao(self) -> str:
        return self.__observacao

    def get_lote(self) -> Lote:
        return self.__lote
    
    def get_veiculo(self) -> Veiculo:
        return self.__veiculo

    def get_empresa(self) -> Empresa:
        return self.__empresa

    def get_manutencao(self) -> Manutencao:
        return self.__manutencao

    # Setters
    def set_id_log(self, id_log:int):
        self.__id_log = id_log

    def set_data_evento(self, data_evento:datetime):
        self.__data_evento = data_evento

    def set_tipo_evento(self, tipo_evento:str):
        self.__tipo_evento = tipo_evento

    def set_observacao(self, observacao:str):
        self.__observacao = observacao

    def set_lote(self, lote:Lote):
        self.__lote = lote

    def set_veiculo(self, veiculo:Veiculo):
        self.__veiculo = veiculo

    def set_empresa(self, empresa:Empresa):
        self.__empresa = empresa

    def set_manutencao(self, manutencao:Manutencao):
        self.__manutencao = manutencao

    # To String
    def to_string(self) -> str:
        # Lida com os campos que podem ser nulos para evitar erros
        lote_str = self.get_lote().get_codigo_lote() if self.get_lote() else "N/A"
        veiculo_str = self.get_veiculo().get_placa() if self.get_veiculo() else "N/A"
        
        return (f"ID Log: {self.get_id_log()} | Data: {self.get_data_evento().strftime('%d/%m/%Y %H:%M')} | "
                f"Evento: {self.get_tipo_evento()} | Lote: {lote_str} | Veículo: {veiculo_str}")
