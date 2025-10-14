from src.model.empresa import Empresa
from src.model.contato import Contato

class EmpresaContato:
    def __init__(self, empresa:Empresa, contato:Contato):
        self.__empresa = empresa
        self.__contato = contato

    # Getters
    def get_empresa(self) -> Empresa: 
        return self.__empresa
    def get_contato(self) -> Contato: 
        return self.__contato

    # Setters
    def set_empresa(self, empresa:Empresa): 
        self.__empresa = empresa
    def set_contato(self, contato:Contato): 
        self.__contato = contato

    # To String
    def to_string(self) -> str:
        nome_empresa = self.get_empresa().get_nome_fantasia() if self.get_empresa() else "N/A"
        nome_contato = self.get_contato().get_nome_contato() if self.get_contato() else "N/A"
        return f"Empresa: {nome_empresa} | Contato: {nome_contato}"
