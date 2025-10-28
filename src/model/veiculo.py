from src.model.empresa import Empresa

class Veiculo:
    def __init__(self, id_veiculo:int, placa:str, frota:str, empresa:Empresa):
        self.__id_veiculo = id_veiculo
        self.__placa = placa
        self.__frota = frota
        self.__empresa = empresa

    def get_id_veiculo(self) -> int: 
        return self.__id_veiculo
    def get_placa(self) -> str: 
        return self.__placa
    def get_frota(self) -> str: 
        return self.__frota
    def get_empresa(self) -> Empresa: 
        return self.__empresa

    def set_id_veiculo(self, id_veiculo:int): 
        self.__id_veiculo = id_veiculo
    def set_placa(self, placa:str): 
        self.__placa = placa
    def set_frota(self, frota:str): 
        self.__frota = frota
    def set_empresa(self, empresa:Empresa): 
        self.__empresa = empresa

    def to_string(self) -> str:
        return f"ID: {self.get_id_veiculo()} | Placa: {self.get_placa()} | Frota: {self.get_frota()}"
