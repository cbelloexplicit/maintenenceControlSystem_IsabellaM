from model.Tecnico import Tecnico
from model.Empresa import Empresa

class TecnicoEmpresa:
    def __init__(self, tecnico:Tecnico, empresa:Empresa):
        self.__tecnico = tecnico
        self.__empresa = empresa

    # Getters
    def get_tecnico(self) -> Tecnico: 
        return self.__tecnico
    def get_empresa(self) -> Empresa: 
        return self.__empresa

    # Setters
    def set_tecnico(self, tecnico:Tecnico): 
        self.__tecnico = tecnico
    def set_empresa(self, empresa:Empresa): 
        self.__empresa = empresa
    
    # To String
    def to_string(self) -> str:
        nome_tecnico = self.get_tecnico().get_contato().get_nome_contato() if self.get_tecnico() and self.get_tecnico().get_contato() else "N/A"
        nome_empresa = self.get_empresa().get_nome_fantasia() if self.get_empresa() else "N/A"
        return f"Técnico: {nome_tecnico} | Empresa: {nome_empresa}"
