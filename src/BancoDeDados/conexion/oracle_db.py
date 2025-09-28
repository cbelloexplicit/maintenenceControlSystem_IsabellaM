# Arquivo: conexion/oracle_db.py

import oracledb

class OracleDB:
    def __init__(self):
        # Substitua com suas credenciais do Oracle
        self._user = "projetoDados"
        self._password = "isaqwe123"  # A senha que você definiu para o usuário 'projetodados'
        self._host = "localhost"
        self._port = "1521"
        self._service_name = "XEPDB1"
        
        self.connection = None
        self.cursor = None

    def connect(self):
        """Estabelece a conexão com o banco de dados Oracle."""
        try:
            dsn = oracledb.makedsn(self._host, self._port, service_name=self._service_name)
            self.connection = oracledb.connect(user=self._user, password=self._password, dsn=dsn)
            self.cursor = self.connection.cursor()
            print("Conexão com o Oracle DB estabelecida com sucesso!")
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao Oracle DB: {e}")
            # Levanta a exceção para que a chamada saiba que a conexão falhou
            raise

    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexão com o Oracle DB fechada.")

    def execute_query(self, query: str, **params):
        """Executa uma query no banco de dados (para INSERT, UPDATE, DELETE)."""
        try:
            self.connect()
            self.cursor.execute(query, params)
            self.connection.commit()  # Confirma a transação
        except oracledb.DatabaseError as e:
            print(f"Erro ao executar a query: {e}")
            # Em caso de erro, reverte a transação
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            self.disconnect()

    # Você pode adicionar um método para SELECTs aqui depois