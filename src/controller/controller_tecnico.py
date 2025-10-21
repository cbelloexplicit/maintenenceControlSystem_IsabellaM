from src.conexion.oracledb import OracleDB
from src.model.tecnico import Tecnico
from src.model.contato import Contato


class Controller_Tecnico:

    def __init__(self):
        pass

    def inserir_tecnico(self, novo_tecnico: Tecnico) -> bool:
        """ Insere um novo técnico no banco de dados com status 'ATIVO' por padrão. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO tecnicos (id_tecnico, local, id_contato, status) 
                    VALUES (seq_tecnicos.nextval, :local, :id_contato, 'ATIVO')
                    """
            params = {
                'local': novo_tecnico.get_local(),
                'id_contato': novo_tecnico.get_contato().get_id_contato()
            }
            db.execute_write_query(query, params)
            print("Técnico inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir técnico: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_tecnicos(self, apenas_ativos: bool = True) -> list[Tecnico]:
        """
        Lista os técnicos. Por padrão, lista apenas os ativos.
        Se apenas_ativos for False, lista todos (ativos e inativos).
        """
        db = OracleDB()
        lista_tecnicos = []
        try:
            db.connect()
            query = """
                    SELECT t.id_tecnico, t.local, t.status,
                           c.id_contato, c.nome_contato, c.email_contato, c.telefone
                    FROM tecnicos t
                    JOIN contatos c ON t.id_contato = c.id_contato
                    """
            if apenas_ativos:
                query += " WHERE t.status = 'ATIVO'"

            query += " ORDER BY c.nome_contato"

            resultado = db.execute_select(query)

            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[3], nome_contato=linha[4], email_contato=linha[5],
                                      telefone=linha[6])
                    tecnico = Tecnico(id_tecnico=linha[0], local=linha[1], status=linha[2], contato=contato)
                    lista_tecnicos.append(tecnico)

            return lista_tecnicos
        except Exception as e:
            print(f"Erro ao listar técnicos: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def atualizar_tecnico(self, tecnico_atualizado: Tecnico) -> bool:
        """ Atualiza os dados de um técnico existente. Não altera o status. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE tecnicos 
                    SET local = :local, id_contato = :id_contato
                    WHERE id_tecnico = :id_tecnico
                    """
            params = {
                'local': tecnico_atualizado.get_local(),
                'id_contato': tecnico_atualizado.get_contato().get_id_contato(),
                'id_tecnico': tecnico_atualizado.get_id_tecnico()
            }
            db.execute_write_query(query, params)
            print("Técnico atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar técnico: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def inativar_tecnico(self, id_tecnico: int) -> bool:
        """ Realiza o 'soft delete' de um técnico, mudando seu status para 'INATIVO'. """
        return self._alterar_status_tecnico(id_tecnico, 'INATIVO')

    def ativar_tecnico(self, id_tecnico: int) -> bool:
        """ Ativa um técnico, mudando seu status para 'ATIVO'. """
        return self._alterar_status_tecnico(id_tecnico, 'ATIVO')


    def remover_tecnico(self, id_tecnico: int) -> bool:
        """
        Primeiro, desassocia de todas as empresas.
        """
        db = OracleDB()
        try:
            db.connect()

            # Verifica se o técnico está em uso em visitas (regra de negócio para impedir remoção)
            query_check = "SELECT 1 FROM VISITAS_TECNICAS WHERE id_tecnico = :id_tecnico"
            if db.cursor.execute(query_check, {'id_tecnico': id_tecnico}).fetchone():
                print(
                    f"Erro: Não é possível remover o técnico (ID: {id_tecnico}), pois ele possui visitas técnicas registradas em seu histórico.")
                return False

            # Remove associações da tabela de junção
            query_disassociate = "DELETE FROM tecnicos_empresas WHERE id_tecnico = :id_tecnico"
            db.execute_write_query(query_disassociate, {'id_tecnico': id_tecnico})

            # Remove o técnico da tabela principal
            query_delete = "DELETE FROM tecnicos WHERE id_tecnico = :id_tecnico"
            db.execute_write_query(query_delete, {'id_tecnico': id_tecnico})

            print(f"Técnico (ID: {id_tecnico}) removido permanentemente com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover técnico: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def associar_tecnico_empresa(self, id_tecnico: int, id_empresa: int) -> bool:
        """ Cria uma associação entre um técnico e uma empresa na tabela de junção. """
        db = OracleDB()
        try:
            db.connect()
            query = "INSERT INTO tecnicos_empresas (id_tecnico, id_empresa) VALUES (:id_tecnico, :id_empresa)"
            params = {'id_tecnico': id_tecnico, 'id_empresa': id_empresa}
            db.execute_write_query(query, params)
            print(f"Técnico {id_tecnico} associado à empresa {id_empresa} com sucesso!")
            return True
        except Exception as e:
            # O erro mais comum aqui é 'unique constraint violated' se a associação já existir.
            print(f"Erro ao associar técnico à empresa: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def desassociar_tecnico_empresa(self, id_tecnico: int, id_empresa: int) -> bool:
        """ Remove uma associação entre um técnico e uma empresa. """
        db = OracleDB()
        try:
            db.connect()
            query = "DELETE FROM tecnicos_empresas WHERE id_tecnico = :id_tecnico AND id_empresa = :id_empresa"
            params = {'id_tecnico': id_tecnico, 'id_empresa': id_empresa}
            db.execute_write_query(query, params)
            print(f"Técnico {id_tecnico} desassociado da empresa {id_empresa} com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao desassociar técnico da empresa: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def buscar_tecnicos_por_nome(self, nome: str) -> list[Tecnico]:
        """
        Busca técnicos ATIVOS cujo nome do contato contenha o texto fornecido.
        A busca é case-insensitive (não diferencia maiúsculas de minúsculas).
        Retorna uma lista de objetos Tecnico.
        """
        db = OracleDB()
        lista_tecnicos = []
        try:
            db.connect()
            # UPPER() torna a busca case-insensitive.
            # O operador LIKE com '%' busca por nomes que CONTÊM o texto.
            query = """
                    SELECT t.id_tecnico, t.local, t.status,
                           c.id_contato, c.nome_contato, c.email_contato, c.telefone
                    FROM tecnicos t
                    JOIN contatos c ON t.id_contato = c.id_contato
                    WHERE t.status = 'ATIVO' AND UPPER(c.nome_contato) LIKE UPPER(:nome_param)
                    ORDER BY c.nome_contato
                    """

            # Prepara o parâmetro para a busca com LIKE
            params = {'nome_param': f'%{nome}%'}

            resultado = db.execute_select(query, params)

            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[3], nome_contato=linha[4], email_contato=linha[5],
                                      telefone=linha[6])
                    # É importante recriar o objeto com todos os seus atributos, incluindo o status
                    tecnico = Tecnico(id_tecnico=linha[0], local=linha[1], status=linha[2], contato=contato)
                    lista_tecnicos.append(tecnico)

            return lista_tecnicos
        except Exception as e:
            print(f"Erro ao buscar técnicos por nome: {e}")
            return []
        finally:
            if db.connection:
                db.close()