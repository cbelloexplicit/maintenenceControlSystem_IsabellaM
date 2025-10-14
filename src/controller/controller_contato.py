from src.conexion.oracledb import OracleDB
from src.model.contato import Contato

class Controller_Contato:
    def __init__(self):
        pass

    def inserir_contato(self, novo_contato: Contato) -> bool:
        """
        Insere um novo contato no banco de dados.
        A validação de e-mail E/OU telefone é garantida pela CONSTRAINT no banco.
        """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO contatos (id_contato, nome_contato, email_contato, telefone) 
                    VALUES (seq_contatos.nextval, :nome, :email, :telefone)
                    """
            params = {
                'nome': novo_contato.get_nome_contato(),
                'email': novo_contato.get_email_contato(),
                'telefone': novo_contato.get_telefone()
            }
            db.execute_write_query(query, params)
            print("Contato inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir contato: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_contato(self, id_contato: int) -> bool:
        """ Remove um contato do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o contato está sendo usado em outras tabelas
            tabelas_dependentes = ["TECNICOS", "EMPRESA_CONTATOS"]
            for tabela in tabelas_dependentes:
                query_check = f"SELECT 1 FROM {tabela} WHERE id_contato = :id_contato"
                if db.cursor.execute(query_check, {'id_contato': id_contato}).fetchone():
                    print(
                        f"Erro: Não é possível remover o contato (ID: {id_contato}), pois ele está em uso na tabela '{tabela}'.")
                    return False

            # Se não houver dependências, remove o contato
            query_delete = "DELETE FROM contatos WHERE id_contato = :id_contato"
            db.execute_write_query(query_delete, {'id_contato': id_contato})
            print(f"Contato (ID: {id_contato}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover contato: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_contato(self, contato_atualizado: Contato) -> bool:
        """ Atualiza os dados de um contato existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE contatos
                    SET nome_contato = :nome, email_contato = :email, telefone = :telefone
                    WHERE id_contato = :id_contato
                    """
            params = {
                'nome': contato_atualizado.get_nome_contato(),
                'email': contato_atualizado.get_email_contato(),
                'telefone': contato_atualizado.get_telefone(),
                'id_contato': contato_atualizado.get_id_contato()
            }
            db.execute_write_query(query, params)
            print("Contato atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar contato: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_contatos(self) -> list[Contato]:
        """ Lista todos os contatos cadastrados. """
        db = OracleDB()
        lista_contatos = []
        try:
            db.connect()
            query = "SELECT id_contato, nome_contato, email_contato, telefone FROM contatos ORDER BY nome_contato"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[0], nome_contato=linha[1], email_contato=linha[2],
                                      telefone=linha[3])
                    lista_contatos.append(contato)
            return lista_contatos
        except Exception as e:
            print(f"Erro ao listar contatos: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_contato_por_nome(self, nome: str) -> list[Contato]:
        """ Busca contatos cujo nome contenha o texto fornecido. """
        db = OracleDB()
        lista_contatos = []
        try:
            db.connect()
            query = """
                    SELECT id_contato, nome_contato, email_contato, telefone FROM contatos 
                    WHERE UPPER(nome_contato) LIKE UPPER(:nome_param)
                    ORDER BY nome_contato
                    """
            params = {'nome_param': f'%{nome}%'}
            resultado = db.execute_select(query, params)
            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[0], nome_contato=linha[1], email_contato=linha[2],
                                      telefone=linha[3])
                    lista_contatos.append(contato)
            return lista_contatos
        except Exception as e:
            print(f"Erro ao buscar contatos por nome: {e}")
            return []
        finally:
            if db.connection:
                db.close()