
from src.conexion.oracledb import OracleDB
from src.model.lot import Lot


class Controller_Lot:

    def __init__(self):
        pass

    def inserir_lot(self, novo_lot: Lot) -> bool:
        """ Insere um novo lote (dispositivo) no banco de dados. """
        db = OracleDB()
        try:
            # Verifica se o código do lote já existe
            if self.buscar_lote_por_codigo(novo_lot.get_codigo_lot()):
                print(f"Erro ao inserir: O código de lote '{novo_lot.get_codigo_lot()}' já está cadastrado.")
                return False

            db.connect()
            query = """
                    INSERT INTO lots (id_lot, codigo_lot, obs_lot) 
                    VALUES (seq_lots.nextval, :codigo, :obs)
                    """
            params = {
                'codigo': novo_lot.get_codigo_lot(),
                'obs': novo_lot.get_obs_lot()
            }
            db.execute_write_query(query, params)
            print("Lote (Dispositivo) inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir lote: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_lots(self) -> list[Lot]:
        """ Lista todos os lotes (dispositivos) cadastrados. """
        db = OracleDB()
        lista_lotes = []
        try:
            db.connect()
            query = "SELECT id_lot, codigo_lot, obs_lot FROM lots ORDER BY codigo_lot"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    lot = Lot(id_lot=linha[0], codigo_lot=linha[1], obs_lot=linha[2])
                    lista_lotes.append(lot)
            return lista_lotes
        except Exception as e:
            print(f"Erro ao listar lotes: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_lote_por_codigo(self, codigo_lot: str) -> Lot | None:
        """ Busca um lote (dispositivo) específico pelo seu código (case-insensitive). """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT id_lot, codigo_lot, obs_lot FROM lots 
                    WHERE UPPER(codigo_lot) = UPPER(:codigo)
                    """
            params = {'codigo': codigo_lot}
            resultado = db.execute_select(query, params)
            if resultado:
                linha = resultado[0]
                lote = Lot(id_lot=linha[0], codigo_lot=linha[1], obs_lot=linha[2])
                return lote
            return None
        except Exception as e:
            print(f"Erro ao buscar lote por código: {e}")
            return None
        finally:
            if db.connection:
                db.close()

    def atualizar_lot(self, lote_atualizado: Lot) -> bool:
        """ Atualiza os dados de um lote (dispositivo) existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE lots
                    SET codigo_lot = :codigo, obs_lot = :obs
                    WHERE id_lot = :id_lot
                    """
            params = {
                'codigo': lote_atualizado.get_codigo_lot(),
                'obs': lote_atualizado.get_obs_lot(),
                'id_lot': lote_atualizado.get_id_lot()
            }
            db.execute_write_query(query, params)
            print("Lote (Dispositivo) atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar lote: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_lot(self, id_lot: int) -> bool:
        """ Remove um lote (dispositivo) do banco, após verificar se ele não possui histórico. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o lote possui algum registro na tabela de log
            query_check = "SELECT 1 FROM LOG_LOT WHERE id_lot = :id_lot"
            if db.cursor.execute(query_check, {'id_lot': id_lot}).fetchone():
                print(
                    f"Erro: Não é possível remover o lote (ID: {id_lot}), pois ele possui um histórico de eventos registrado.")
                return False

            # Se não houver dependências, remove o lote
            query_delete = "DELETE FROM lots WHERE id_lot = :id_lot"
            db.execute_write_query(query_delete, {'id_lot': id_lot})
            print(f"Lote (ID: {id_lot}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover lote: {e}")
            return False
        finally:
            if db.connection:
                db.close()