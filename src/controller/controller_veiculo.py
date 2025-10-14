from src.conexion.oracledb import OracleDB
from src.model.veiculo import Veiculo
from src.model.empresa import Empresa
from src.model.lot import Lot

class Controller_Veiculo:
    def __init__(self):
        pass

    def inserir_veiculo(self, novo_veiculo: Veiculo) -> bool:
        """ Insere um novo veículo no banco de dados. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO veiculos (id_veiculo, placa, frota, id_empresa) 
                    VALUES (seq_veiculos.nextval, :placa, :frota, :id_empresa)
                    """
            params = {
                'placa': novo_veiculo.get_placa(),
                'frota': novo_veiculo.get_frota(),
                'id_empresa': novo_veiculo.get_empresa().get_id_empresa()
            }
            db.execute_write_query(query, params)
            print("Veículo inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir veículo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_veiculo(self, id_veiculo: int) -> bool:
        """ Remove um veículo do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o veículo está sendo usado em outras tabelas
            tabelas_dependentes = ["DEFEITOS", "LOG_LOT"]
            for tabela in tabelas_dependentes:
                query_check = f"SELECT 1 FROM {tabela} WHERE id_veiculo = :id_veiculo"
                if db.cursor.execute(query_check, {'id_veiculo': id_veiculo}).fetchone():
                    print(
                        f"Erro: Não é possível remover o veículo (ID: {id_veiculo}), pois ele possui registros na tabela '{tabela}'.")
                    return False

            # Se não houver dependências, remove o veículo
            query_delete = "DELETE FROM veiculos WHERE id_veiculo = :id_veiculo"
            db.execute_write_query(query_delete, {'id_veiculo': id_veiculo})
            print(f"Veículo (ID: {id_veiculo}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover veículo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_veiculo(self, veiculo_atualizado: Veiculo) -> bool:
        """ Atualiza os dados de um veículo existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE veiculos
                    SET placa = :placa, frota = :frota, id_empresa = :id_empresa
                    WHERE id_veiculo = :id_veiculo
                    """
            params = {
                'placa': veiculo_atualizado.get_placa(),
                'frota': veiculo_atualizado.get_frota(),
                'id_empresa': veiculo_atualizado.get_empresa().get_id_empresa(),
                'id_veiculo': veiculo_atualizado.get_id_veiculo()
            }
            db.execute_write_query(query, params)
            print("Veículo atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar veículo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_veiculos(self) -> list[Veiculo]:
        """ Lista todos os veículos cadastrados, incluindo dados da empresa. """
        db = OracleDB()
        lista_veiculos = []
        try:
            db.connect()
            query = """
                    SELECT v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM veiculos v
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    ORDER BY v.placa
                    """
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    empresa = Empresa(id_empresa=linha[3], nome_fantasia=linha[4], endereco=linha[5])
                    veiculo = Veiculo(id_veiculo=linha[0], placa=linha[1], frota=linha[2], empresa=empresa)
                    lista_veiculos.append(veiculo)
            return lista_veiculos
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_veiculo_por_placa(self, placa: str) -> Veiculo | None:
        """ Busca um veículo específico pela sua placa (case-insensitive). """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM veiculos v
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    WHERE UPPER(v.placa) = UPPER(:placa)
                    """
            resultado = db.execute_select(query, {'placa': placa})
            if resultado:
                linha = resultado[0]
                empresa = Empresa(id_empresa=linha[3], nome_fantasia=linha[4], endereco=linha[5])
                veiculo = Veiculo(id_veiculo=linha[0], placa=linha[1], frota=linha[2], empresa=empresa)
                return veiculo
            return None
        except Exception as e:
            print(f"Erro ao buscar veículo por placa: {e}")
            return None
        finally:
            if db.connection:
                db.close()

    def buscar_lote_instalado(self, id_veiculo: int) -> Lot | None:
        """
        Verifica qual dispositivo (lote) está atualmente instalado em um veículo.
        Retorna o objeto Lote se houver um instalado, ou None caso contrário.
        """
        db = OracleDB()
        try:
            db.connect()
            # Query complexa para encontrar o último evento de INSTALACAO que não foi seguido por uma DESINSTALACAO para o mesmo lote/veículo.
            query = """
                    SELECT l.id_lot, l.codigo_lot, l.obs_lot
                    FROM lots l
                    JOIN (
                        -- Subquery para encontrar a última instalação para cada veículo
                        SELECT id_veiculo, id_lot, MAX(data_evento) as ultima_instalacao
                        FROM log_lot
                        WHERE id_veiculo = :id_veiculo AND id_catalogo_eventos = (SELECT id_catalogo_eventos FROM catalogo_eventos WHERE codigo_evento = 'INSTALACAO')
                        GROUP BY id_veiculo, id_lot
                    ) ultimas_instalacoes ON l.id_lot = ultimas_instalacoes.id_lot
                    WHERE NOT EXISTS (
                        -- Verifica se NÃO existe um evento de desinstalação POSTERIOR à última instalação
                        SELECT 1
                        FROM log_lot desinstal
                        WHERE desinstal.id_lot = l.id_lot
                          AND desinstal.id_veiculo = :id_veiculo
                          AND desinstal.id_catalogo_eventos = (SELECT id_catalogo_eventos FROM catalogo_eventos WHERE codigo_evento = 'DESINSTALACAO')
                          AND desinstal.data_evento > ultimas_instalacoes.ultima_instalacao
                    )
                    FETCH FIRST 1 ROWS ONLY
                    """
            resultado = db.execute_select(query, {'id_veiculo': id_veiculo})
            if resultado:
                linha = resultado[0]
                lot = Lot(id_lot=linha[0], codigo_lot=linha[1], obs_lot=linha[2])
                return lot
            return None
        except Exception as e:
            print(f"Erro ao buscar lote instalado: {e}")
            return None
        finally:
            if db.connection:
                db.close()