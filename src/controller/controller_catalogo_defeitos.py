from src.conexion.oracledb import OracleDB
from src.model.catalogo_defeito import CatalogoDefeitos


class Controller_Catalogo_Defeitos:

    def __init__(self):
        pass

    def inserir_defeito(self, novo_defeito: CatalogoDefeitos) -> bool:
        """ Insere um novo defeito no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o código do defeito já existe para evitar duplicatas
            if self.buscar_defeito_por_codigo(novo_defeito.get_codigo_defeito()):
                print(f"Erro ao inserir: O código de defeito '{novo_defeito.get_codigo_defeito()}' já existe.")
                return False

            query = """
                    INSERT INTO catalogo_defeitos (id_catalogo_defeito, codigo_defeito, descricao_defeito) 
                    VALUES (seq_catalogo_defeitos.nextval, :codigo, :descricao)
                    """
            params = {
                'codigo': novo_defeito.get_codigo_defeito(),
                'descricao': novo_defeito.get_descricao_defeito()
            }
            db.execute_write_query(query, params)
            print("Defeito do catálogo inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir defeito no catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_defeito(self, id_catalogo_defeito: int) -> bool:
        """ Remove um defeito do catálogo, após verificar se ele não está em uso. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o defeito está sendo usado na tabela de DEFEITOS
            query_check = "SELECT 1 FROM DEFEITOS WHERE id_catalogo_defeito = :id_defeito"
            if db.cursor.execute(query_check, {'id_defeito': id_catalogo_defeito}).fetchone():
                print(
                    f"Erro: Não é possível remover o defeito (ID: {id_catalogo_defeito}), pois ele está em uso em registros de defeitos reportados.")
                return False

            query_delete = "DELETE FROM catalogo_defeitos WHERE id_catalogo_defeito = :id_defeito"
            db.execute_write_query(query_delete, {'id_defeito': id_catalogo_defeito})
            print(f"Defeito do catálogo (ID: {id_catalogo_defeito}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover defeito do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_defeito(self, defeito_atualizado: CatalogoDefeitos) -> bool:
        """ Atualiza os dados de um defeito existente no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE catalogo_defeitos
                    SET codigo_defeito = :codigo, descricao_defeito = :descricao
                    WHERE id_catalogo_defeito = :id_defeito
                    """
            params = {
                'codigo': defeito_atualizado.get_codigo_defeito(),
                'descricao': defeito_atualizado.get_descricao_defeito(),
                'id_defeito': defeito_atualizado.get_id_catalogo_defeito()
            }
            db.execute_write_query(query, params)
            print("Defeito do catálogo atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar defeito do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_defeitos(self) -> list[CatalogoDefeitos]:
        """ Lista todos os defeitos do catálogo. """
        db = OracleDB()
        lista_defeitos = []
        try:
            db.connect()
            query = "SELECT id_catalogo_defeito, codigo_defeito, descricao_defeito FROM catalogo_defeitos ORDER BY codigo_defeito"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    defeito = CatalogoDefeitos(id_catalogo_defeito=linha[0], codigo_defeito=linha[1],
                                              descricao_defeito=linha[2])
                    lista_defeitos.append(defeito)
            return lista_defeitos
        except Exception as e:
            print(f"Erro ao listar defeitos do catálogo: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_defeito_por_codigo(self, codigo_defeito: str) -> CatalogoDefeitos | None:
        """ Busca um defeito específico no catálogo pelo seu código (case-insensitive). """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT id_catalogo_defeito, codigo_defeito, descricao_defeito FROM catalogo_defeitos 
                    WHERE UPPER(codigo_defeito) = UPPER(:codigo)
                    """
            params = {'codigo': codigo_defeito}
            resultado = db.execute_select(query, params)
            if resultado:
                linha = resultado[0]
                defeito = CatalogoDefeitos(id_catalogo_defeito=linha[0], codigo_defeito=linha[1],
                                          descricao_defeito=linha[2])
                return defeito
            return None
        except Exception as e:
            print(f"Erro ao buscar defeito por código: {e}")
            return None
        finally:
            if db.connection:
                db.close()