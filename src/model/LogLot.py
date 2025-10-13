from datetime import date
from model.Lot import Lot
from model.Veiculo import Veiculo
from model.Empresa import Empresa
from model.Manutencao import Manutencao
from model.CatalogoEvento import CatalogoEvento

class LogLot:
    def __init__(self, id_log:int, data_evento:date, responsavel_evento:str, obs_evento:str, 
                 lot:Lot, catalogo_eventos:CatalogoEvento, veiculo:Veiculo = None, 
                 empresa:Empresa = None, manutencao:Manutencao = None):
        self.__id_log = id_log
        self.__data_evento = data_evento
        self.__responsavel_evento = responsavel_evento
        self.__obs_evento = obs_evento
        self.__lot = lot
        self.__veiculo = veiculo
        self.__empresa = empresa
        self.__manutencao = manutencao
        self.__catalogo_eventos = catalogo_eventos

    # Getters
    def get_id_log(self) -> int: return self.__id_log
    def get_data_evento(self) -> date: return self.__data_evento
    def get_responsavel_evento(self) -> str: return self.__responsavel_evento
    def get_obs_evento(self) -> str: return self.__obs_evento
    def get_lot(self) -> Lot: return self.__lot
    def get_veiculo(self) -> Veiculo: return self.__veiculo
    def get_empresa(self) -> Empresa: return self.__empresa
    def get_manutencao(self) -> Manutencao: return self.__manutencao
    def get_catalogo_eventos(self) -> CatalogoEvento: return self.__catalogo_eventos

    # Setters
    def set_id_log(self, id_log:int): self.__id_log = id_log
    def set_data_evento(self, data_evento:date): self.__data_evento = data_evento
    def set_responsavel_evento(self, responsavel_evento:str): self.__responsavel_evento = responsavel_evento
    def set_obs_evento(self, obs_evento:str): self.__obs_evento = obs_evento
    def set_lot(self, lot:Lot): self.__lot = lot
    def set_veiculo(self, veiculo:Veiculo): self.__veiculo = veiculo
    def set_empresa(self, empresa:Empresa): self.__empresa = empresa
    def set_manutencao(self, manutencao:Manutencao): self.__manutencao = manutencao
    def set_catalogo_eventos(self, catalogo_eventos:CatalogoEvento): self.__catalogo_eventos = catalogo_eventos

    # To String
    def to_string(self) -> str:
        evento = self.get_catalogo_eventos().get_codigo_evento() if self.get_catalogo_eventos() else "N/A"
        return f"ID: {self.get_id_log()} | Evento: {evento} | Data: {self.get_data_evento()}"
