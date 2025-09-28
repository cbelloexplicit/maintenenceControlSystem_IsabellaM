class Contato:
    def __init__(self, id_contato:str, nome_contato:str, email:str, telefone:str):
        self.__id_contato = id_contato
        self.__nome_contato = nome_contato
        self.__email = email
        self.__telefone = telefone

    # Getters
    def get_id_contato(self) -> str:
        return self.__id_contato

    def get_nome_contato(self) -> str:
        return self.__nome_contato

    def get_email(self) -> str:
        return self.__email

    def get_telefone(self) -> str:
        return self.__telefone

    # Setters
    def set_id_contato(self, id_contato:str):
        self.__id_contato = id_contato

    def set_nome_contato(self, nome_contato:str):
        self.__nome_contato = nome_contato

    def set_email(self, email:str):
        self.__email = email

    def set_telefone(self, telefone:str):
        self.__telefone = telefone

    # To String
    def to_string(self) -> str:
        return f"ID: {self.get_id_contato()} | Nome: {self.get_nome_contato()} | Email: {self.get_email()} | Telefone: {self.get_telefone()}"