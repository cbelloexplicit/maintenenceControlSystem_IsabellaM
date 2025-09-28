from model.visita_tecnica import VisitaTecnica
from model.defeito import Defeito
from model.catalogo_acao import CatalogoAcao

class Manutencao:
    def __init__(self, id_manutencao:int, observacoes_servico:str, visita:VisitaTecnica = None, defeito:Defeito = None, catalogo_acao:CatalogoAcao = None):
        self.__id_manutencao = id_manutencao
        self.__observacoes_servico = observacoes_servico
        self.__visita = visita
        self.__defeito = defeito
        self.__catalogo_acao = catalogo_acao

    # Getters
    def get_id_manutencao(self) -> int:
        return self.__id_manutencao

    def get_observacoes_servico(self) -> str:
        return self.__observacoes_servico

    def get_visita(self) -> VisitaTecnica:
        return self.__visita

    def get_defeito(self) -> Defeito:
        return self.__defeito

    def get_catalogo_acao(self) -> CatalogoAcao:
        return self.__catalogo_acao

    # Setters
    def set_id_manutencao(self, id_manutencao:int):
        self.__id_manutencao = id_manutencao

    def set_observacoes_servico(self, observacoes_servico:str):
        self.__observacoes_servico = observacoes_servico

    def set_visita(self, visita:VisitaTecnica):
        self.__visita = visita

    def set_defeito(self, defeito:Defeito):
        self.__defeito = defeito

    def set_catalogo_acao(self, catalogo_acao:CatalogoAcao):
        self.__catalogo_acao = catalogo_acao

    # To String
    def to_string(self) -> str:
        acao_str = self.get_catalogo_acao().get_descricao_acao() if self.get_catalogo_acao() else "N/A"
        defeito_id_str = self.get_defeito().get_id_defeito() if self.get_defeito() else "N/A"
        return f"ID: {self.get_id_manutencao()} | Ação Realizada: {acao_str} | Defeito Atendido (ID): {defeito_id_str}"