import oracledb

class OracleDB:
    def __init__(self):
        self._user = "PROJETODADOS"
        self._password = "Ibl@20me"
        self._host = "localhost"
        self._port = "1521"
        self._service_name = "XEPDB1"

        self.connection = None
        self.cursor = None

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            dsn = oracledb.makedsn(self._host, self._port, service_name=self._service_name)
            self.connection = oracledb.connect(user=self._user, password=self._password, dsn=dsn)
            self.cursor = self.connection.cursor()
            print("Conexão com o Oracle estabelecida com sucesso!")
            return True
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao Oracle: {e}")
            return False

    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexão com o Oracle DB fechada.")

    def execute_query(self, query: str, params: dict = None):
        """Executa uma query no banco de dados (para INSERT, UPDATE, DELETE)."""
        try:
            # Garantir conexão
            if not self.connection:
                self.connect()

            #Executa query
            self.cursor.execute(query, params or {})
            self.connection.commit()
            print("Query executada e comitada com sucesso.")
        except oracledb.DatabaseError as e:
            print(f"Erro ao executar a query: {e}")
            if self.connection:
                self.connection.rollback()
            raise

    def execute_select(self, query: str, params: dict = None):
        """Executa query SELECT e retorna os resultados."""
        try:
            if not self.connection:
                self.connect()
            self.cursor.execute(query, params or {})
            return self.cursor.fetchall()
        except oracledb.DatabaseError as e:
            print(f"Erro ao executar a consulta: {e}")
            raise