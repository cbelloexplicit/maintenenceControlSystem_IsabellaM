from model.VisitaTecnica import VisitaTecnica
from model.CatalogoAcao import CatalogoAcao
from model.Defeito import Defeito

class Manutencao:
    def __init__(self, id_manutencao:int, obs_servico:str, visita:VisitaTecnica, catalogo_acao:CatalogoAcao, defeito:Defeito):
        self.__id_manutencao = id_manutencao
        self.__obs_servico = obs_servico
        self.__visita = visita
        self.__catalogo_acao = catalogo_acao
        self.__defeito = defeito

    # Getters
    def get_id_manutencao(self) -> int: return self.__id_manutencao
    def get_obs_servico(self) -> str: return self.__obs_servico
    def get_visita(self) -> VisitaTecnica: return self.__visita
    def get_catalogo_acao(self) -> CatalogoAcao: return self.__catalogo_acao
    def get_defeito(self) -> Defeito: return self.__defeito

    # Setters
    def set_id_manutencao(self, id_manutencao:int): self.__id_manutencao = id_manutencao
    def set_obs_servico(self, obs_servico:str): self.__obs_servico = obs_servico
    def set_visita(self, visita:VisitaTecnica): self.__visita = visita
    def set_catalogo_acao(self, catalogo_acao:CatalogoAcao): self.__catalogo_acao = catalogo_acao
    def set_defeito(self, defeito:Defeito): self.__defeito = defeito

    # To String
    def to_string(self) -> str:
        acao = self.get_catalogo_acao().get_descricao_acao() if self.get_catalogo_acao() else "N/A"
        id_defeito = self.get_defeito().get_id_defeito() if self.get_defeito() else "N/A"
        return f"ID: {self.get_id_manutencao()} | Ação: {acao} | Defeito ID: {id_defeito}"
