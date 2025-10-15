from src.conexion.oracledb import OracleDB
from src.model.defeito import Defeito
from src.model.catalogo_defeito import CatalogoDefeitos
from src.model.veiculo import Veiculo
from src.model.empresa import Empresa
from datetime import date

class Controller_Defeito:

    def __init__(self):
        pass

    def inserir_defeito(self, novo_defeito: Defeito) -> bool:
        """ Insere um novo defeito reportado no banco de dados. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO defeitos (id_defeito, id_catalogo_defeito, id_veiculo, data_reporte, status_defeito, obs_defeitos) 
                    VALUES (seq_defeitos.nextval, :id_catalogo, :id_veiculo, :data_reporte, :status, :obs)
                    """
            params = {
                'id_catalogo': novo_defeito.get_catalogo_defeito().get_id_catalogo_defeito(),
                'id_veiculo': novo_defeito.get_veiculo().get_id_veiculo(),
                'data_reporte': novo_defeito.get_data_reporte(),
                'status': novo_defeito.get_status_defeito(),
                'obs': novo_defeito.get_obs_defeitos()
            }
            db.execute_write_query(query, params)
            print("Defeito inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir defeito: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_defeito_em_veiculo(self, id_defeito: int) -> bool:
        """ Remove um defeito do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            query_check = "SELECT 1 FROM MANUTENCOES WHERE id_defeito = :id_defeito"
            if db.cursor.execute(query_check, {'id_defeito': id_defeito}).fetchone():
                print(f"Erro: Não é possível remover o defeito (ID: {id_defeito}), pois ele possui manutenções associadas.")
                return False

            query_delete = "DELETE FROM defeitos WHERE id_defeito = :id_defeito"
            db.execute_write_query(query_delete, {'id_defeito': id_defeito})
            print(f"Defeito (ID: {id_defeito}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover defeito: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_defeito(self, defeito_atualizado: Defeito) -> bool:
        """ Atualiza os dados de um defeito existente, como status ou observações. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE defeitos
                    SET id_catalogo_defeito = :id_catalogo,
                        id_veiculo = :id_veiculo,
                        data_reporte = :data_reporte,
                        status_defeito = :status,
                        obs_defeitos = :obs
                    WHERE id_defeito = :id_defeito
                    """
            params = {
                'id_catalogo': defeito_atualizado.get_catalogo_defeito().get_id_catalogo_defeito(),
                'id_veiculo': defeito_atualizado.get_veiculo().get_id_veiculo(),
                'data_reporte': defeito_atualizado.get_data_reporte(),
                'status': defeito_atualizado.get_status_defeito(),
                'obs': defeito_atualizado.get_obs_defeitos(),
                'id_defeito': defeito_atualizado.get_id_defeito()
            }
            db.execute_write_query(query, params)
            print("Defeito atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar defeito: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_defeitos_em_veiculo(self, id_veiculo: int) -> list[Defeito]:
        """ Lista todos os defeitos reportados para um veículo específico. """
        db = OracleDB()
        lista_defeitos = []
        try:
            db.connect()
            query = """
                    SELECT d.id_defeito, d.data_reporte, d.status_defeito, d.obs_defeitos,
                           cd.id_catalogo_defeito, cd.codigo_defeito, cd.descricao_defeito,
                           v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM defeitos d
                    JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    WHERE d.id_veiculo = :id_veiculo
                    ORDER BY d.data_reporte DESC
                    """
            resultado = db.execute_select(query, {'id_veiculo': id_veiculo})
            if resultado:
                for linha in resultado:
                    catalogo = CatalogoDefeitos(id_catalogo_defeito=linha[4], codigo_defeito=linha[5], descricao_defeito=linha[6])
                    empresa = Empresa(id_empresa=linha[10], nome_fantasia=linha[11], endereco=linha[12])
                    veiculo = Veiculo(id_veiculo=linha[7], placa=linha[8], frota=linha[9], empresa=empresa)
                    defeito = Defeito(id_defeito=linha[0], data_reporte=linha[1], status_defeito=linha[2], obs_defeitos=linha[3],
                                      catalogo_defeito=catalogo, veiculo=veiculo)
                    lista_defeitos.append(defeito)
            return lista_defeitos
        except Exception as e:
            print(f"Erro ao listar defeitos do veículo: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def listar_veiculos_com_defeito_x(self, id_catalogo_defeito: int) -> list[Veiculo]:
        """ Lista todos os veículos que possuem um defeito específico (do catálogo) reportado. """
        db = OracleDB()
        lista_veiculos = []
        try:
            db.connect()
            query = """
                    SELECT DISTINCT v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM veiculos v
                    JOIN defeitos d ON v.id_veiculo = d.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    WHERE d.id_catalogo_defeito = :id_catalogo
                    ORDER BY v.placa
                    """
            resultado = db.execute_select(query, {'id_catalogo': id_catalogo_defeito})
            if resultado:
                for linha in resultado:
                    empresa = Empresa(id_empresa=linha[3], nome_fantasia=linha[4], endereco=linha[5])
                    veiculo = Veiculo(id_veiculo=linha[0], placa=linha[1], frota=linha[2], empresa=empresa)
                    lista_veiculos.append(veiculo)
            return lista_veiculos
        except Exception as e:
            print(f"Erro ao listar veículos com defeito específico: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def relatorio_contagem_defeitos_por_empresa(self) -> list[dict]:
        """ Gera um relatório com a contagem de defeitos por empresa. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT e.nome_fantasia, COUNT(d.id_defeito) as total_defeitos
                    FROM defeitos d
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    GROUP BY e.nome_fantasia
                    ORDER BY total_defeitos DESC
                    """
            resultado = db.execute_select(query)
            # Retorna uma lista de dicionários para fácil manipulação na interface
            return [{'empresa': linha[0], 'total_defeitos': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório de defeitos por empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()