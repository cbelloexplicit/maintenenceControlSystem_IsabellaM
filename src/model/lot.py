class Lot:
    def __init__(self, id_lot:int, codigo_lot:str, obs_lot:str = None):
        self.__id_lot = id_lot
        self.__codigo_lot = codigo_lot
        self.__obs_lot = obs_lot

    def get_id_lot(self) -> int: return self.__id_lot
    def get_codigo_lot(self) -> str: return self.__codigo_lot
    def get_obs_lot(self) -> str: return self.__obs_lot

    def set_id_lot(self, id_lot:int): self.__id_lot = id_lot
    def set_codigo_lot(self, codigo_lot:str): self.__codigo_lot = codigo_lot
    def set_obs_lot(self, obs_lot:str): self.__obs_lot = obs_lot

    def to_string(self) -> str:
        return f"ID: {self.get_id_lot()} | Código: {self.get_codigo_lot()}"
