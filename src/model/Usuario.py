    class Usuario:
        def __init__(self, id_usuario:int, nome_completo:str, email_usuario:str, senha_hash:str):
            self.__id_usuario = id_usuario
            self.__nome_completo = nome_completo
            self.__email_usuario = email_usuario
            self.__senha_hash = senha_hash

        # Getters
        def get_id_usuario(self) -> int: 
            return self.__id_usuario
        def get_nome_completo(self) -> str: 
            return self.__nome_completo
        def get_email_usuario(self) -> str: 
            return self.__email_usuario
        def get_senha_hash(self) -> str: 
            return self.__senha_hash

        # Setters
        def set_id_usuario(self, id_usuario:int): 
            self.__id_usuario = id_usuario
        def set_nome_completo(self, nome_completo:str): 
            self.__nome_completo = nome_completo
        def set_email_usuario(self, email_usuario:str): 
            self.__email_usuario = email_usuario
        def set_senha_hash(self, senha_hash:str): 
            self.__senha_hash = senha_hash

        # To String
        def to_string(self) -> str:
            return f"ID: {self.get_id_usuario()} | Nome: {self.get_nome_completo()} | E-mail: {self.get_email_usuario()}"
