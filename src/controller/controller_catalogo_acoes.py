from src.conexion.oracledb import OracleDB
from src.model.catalogo_acoes import CatalogoAcoes


class Controller_Catalogo_Acoes:

    def __init__(self):
        pass

    def inserir_acao(self, nova_acao: CatalogoAcoes) -> bool:
        """ Insere uma nova ação no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o código da ação já existe para evitar duplicatas
            if self.buscar_acao_por_codigo(nova_acao.get_codigo_acao()):
                print(f"Erro ao inserir: O código de ação '{nova_acao.get_codigo_acao()}' já existe.")
                return False

            query = """
                    INSERT INTO catalogo_acoes (id_catalogo_acao, codigo_acao, descricao_acao) 
                    VALUES (seq_catalogo_acoes.nextval, :codigo, :descricao)
                    """
            params = {
                'codigo': nova_acao.get_codigo_acao(),
                'descricao': nova_acao.get_descricao_acao()
            }
            db.execute_write_query(query, params)
            print("Ação do catálogo inserida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir ação no catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_acao(self, id_catalogo_acao: int) -> bool:
        """ Remove uma ação do catálogo, após verificar se ela não está em uso. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se a ação está sendo usada na tabela de manutenções
            query_check = "SELECT 1 FROM MANUTENCOES WHERE id_catalogo_acao = :id_acao"
            if db.cursor.execute(query_check, {'id_acao': id_catalogo_acao}).fetchone():
                print(
                    f"Erro: Não é possível remover a ação (ID: {id_catalogo_acao}), pois ela está em uso em registros de manutenção.")
                return False

            query_delete = "DELETE FROM catalogo_acoes WHERE id_catalogo_acao = :id_acao"
            db.execute_write_query(query_delete, {'id_acao': id_catalogo_acao})
            print(f"Ação do catálogo (ID: {id_catalogo_acao}) removida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover ação do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_acao(self, acao_atualizada: CatalogoAcoes) -> bool:
        """ Atualiza os dados de uma ação existente no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE catalogo_acoes
                    SET codigo_acao = :codigo, descricao_acao = :descricao
                    WHERE id_catalogo_acao = :id_acao
                    """
            params = {
                'codigo': acao_atualizada.get_codigo_acao(),
                'descricao': acao_atualizada.get_descricao_acao(),
                'id_acao': acao_atualizada.get_id_catalogo_acao()
            }
            db.execute_write_query(query, params)
            print("Ação do catálogo atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar ação do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_acoes(self) -> list[CatalogoAcoes]:
        """ Lista todas as ações do catálogo. """
        db = OracleDB()
        lista_acoes = []
        try:
            db.connect()
            query = "SELECT id_catalogo_acao, codigo_acao, descricao_acao FROM catalogo_acoes ORDER BY codigo_acao"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    acao = CatalogoAcoes(id_catalogo_acao=linha[0], codigo_acao=linha[1], descricao_acao=linha[2])
                    lista_acoes.append(acao)
            return lista_acoes
        except Exception as e:
            print(f"Erro ao listar ações do catálogo: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_acao_por_codigo(self, codigo_acao: str) -> CatalogoAcoes | None:
        """ Busca uma ação específica no catálogo pelo seu código (case-insensitive). """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT id_catalogo_acao, codigo_acao, descricao_acao FROM catalogo_acoes 
                    WHERE UPPER(codigo_acao) = UPPER(:codigo)
                    """
            params = {'codigo': codigo_acao}
            resultado = db.execute_select(query, params)
            if resultado:
                linha = resultado[0]
                acao = CatalogoAcoes(id_catalogo_acao=linha[0], codigo_acao=linha[1], descricao_acao=linha[2])
                return acao
            return None
        except Exception as e:
            print(f"Erro ao buscar ação por código: {e}")
            return None
        finally:
            if db.connection:
                db.close()