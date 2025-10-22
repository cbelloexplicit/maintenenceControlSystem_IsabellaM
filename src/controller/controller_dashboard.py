from src.conexion.oracledb import OracleDB

class ControllerDashboard:
    def __init__(self):
        pass
    def obter_contagem_registros(self) -> dict:
        db = OracleDB()
        contagens = {}
        tabelas_para_contar = [
            "USUARIOS",
            "EMPRESAS",
            "CONTATOS",
            "VEICULOS",
            "TECNICOS",
            "LOTS",
            "DEFEITOS",
            "MANUTENCOES"
        ]

        try:
            db.connect()
            for tabela in tabelas_para_contar:
                query = f"SELECT COUNT(*) FROM {tabela}"
                resultado = db.execute_select(query)
                contagem = resultado[0][0] if resultado else 0
                contagens[tabela] = contagem
            return contagens
        except Exception as e:
            print(f"Erro ao obter registros: {e}")
            return {}
        finally:
            if db.connection:
                db.close()