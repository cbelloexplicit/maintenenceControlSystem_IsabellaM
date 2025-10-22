class CatalogoEventos:
    def __init__(self, id_catalogo_eventos:int, codigo_evento:str):
        self.__id_catalogo_eventos = id_catalogo_eventos
        self.__codigo_evento = codigo_evento

    def get_id_catalogo_eventos(self) -> int: 
        return self.__id_catalogo_eventos
    def get_codigo_evento(self) -> str: 
        return self.__codigo_evento

    def set_id_catalogo_eventos(self, id_catalogo_eventos:int): 
        self.__id_catalogo_eventos = id_catalogo_eventos
    def set_codigo_evento(self, codigo_evento:str): 
        self.__codigo_evento = codigo_evento

    def to_string(self) -> str:
        return f"ID: {self.get_id_catalogo_eventos()} | Evento: {self.get_codigo_evento()}"
