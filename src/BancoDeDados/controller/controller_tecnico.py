from conexion.oracle_db import OracleDB
from model.tecnico import Tecnico

class Controller_Tecnico:

    def __iniciar(self):
        # Cria uma nova conexão com o banco que se fecha automaticamente
        self.db = OracleDB()

    def inserir_tecnico(self, tecnico: Tecnico) -> None:
        """
        Insere um novo técnico no banco de dados.
        A geração do ID é feita pela SEQUENCE do Oracle.
        """
        try:
            self.__iniciar()
            # Cria a query de inserção, usando a sequence para o ID
            query = """
                    INSERT INTO tecnicos (id_tecnico, nome_tecnico) 
                    VALUES (seq_tecnicos.nextval, :nome)
                    """
            # Executa a query, passando os dados do objeto Tecnico
            self.db.execute_query(query, nome=tecnico.get_nome_tecnico())
            print(f"Técnico '{tecnico.get_nome_tecnico()}' inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir técnico: {e}")

    # Aqui você adicionaria os outros métodos: atualizar_tecnico, remover_tecnico, etc.