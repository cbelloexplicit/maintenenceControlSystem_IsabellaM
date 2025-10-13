class Contato:
    def __init__(self, id_contato:int, nome_contato:str, email_contato:str = None, telefone:str = None):
        self.__id_contato = id_contato
        self.__nome_contato = nome_contato
        self.__email_contato = email_contato
        self.__telefone = telefone

    # Getters
    def get_id_contato(self) -> int: 
        return self.__id_contato
    def get_nome_contato(self) -> str: 
        return self.__nome_contato
    def get_email_contato(self) -> str: 
        return self.__email_contato
    def get_telefone(self) -> str: 
        return self.__telefone

    # Setters
    def set_id_contato(self, id_contato:int): 
        self.__id_contato = id_contato
    def set_nome_contato(self, nome_contato:str): 
        self.__nome_contato = nome_contato
    def set_email_contato(self, email_contato:str): 
        self.__email_contato = email_contato
    def set_telefone(self, telefone:str): 
        self.__telefone = telefone

    # To String
    def to_string(self) -> str:
        return f"ID: {self.get_id_contato()} | Nome: {self.get_nome_contato()} | E-mail: {self.get_email_contato()}"
