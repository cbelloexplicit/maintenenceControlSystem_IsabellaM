from src.conexion.oracledb import OracleDB
from src.model.manutencao import Manutencao
from src.model.visita_tecnica import VisitaTecnica
from src.model.catalogo_acoes import CatalogoAcoes
from src.model.defeito import Defeito
# Importações adicionais necessárias para reconstruir os objetos
from src.model.tecnico import Tecnico
from src.model.contato import Contato
from src.model.veiculo import Veiculo
from src.model.empresa import Empresa
from src.model.catalogo_defeito import CatalogoDefeitos


class Controller_Manutencao:

    def __init__(self):
        pass

    def inserir_manutencao(self, nova_manutencao: Manutencao) -> bool:
        """ Insere um novo registro de manutenção no banco de dados. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO manutencoes (id_manutencao, id_visita, id_catalogo_acao, id_defeito, obs_servico) 
                    VALUES (seq_manutencoes.nextval, :id_visita, :id_acao, :id_defeito, :obs)
                    """
            params = {
                'id_visita': nova_manutencao.get_visita().get_id_visita(),
                'id_acao': nova_manutencao.get_catalogo_acao().get_id_catalogo_acao(),
                'id_defeito': nova_manutencao.get_defeito().get_id_defeito(),
                'obs': nova_manutencao.get_obs_servico()
            }
            db.execute_write_query(query, params)
            print("Manutenção inserida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir manutenção: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_manutencao(self, id_manutencao: int) -> bool:
        """ Remove um registro de manutenção do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            query_check = "SELECT 1 FROM LOG_LOT WHERE id_manutencao = :id_manutencao"
            if db.cursor.execute(query_check, {'id_manutencao': id_manutencao}).fetchone():
                print(
                    f"Erro: Não é possível remover a manutenção (ID: {id_manutencao}), pois ela está registrada no histórico de um lote.")
                return False

            query_delete = "DELETE FROM manutenções WHERE id_manutencao = :id_manutencao"
            db.execute_write_query(query_delete, {'id_manutencao': id_manutencao})
            print(f"Manutenção (ID: {id_manutencao}) removida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover manutenção: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_manutencao(self, manutencao_atualizada: Manutencao) -> bool:
        """ Atualiza os dados de uma manutenção existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE manutenções
                    SET id_visita = :id_visita,
                        id_catalogo_acao = :id_acao,
                        id_defeito = :id_defeito,
                        obs_servico = :obs
                    WHERE id_manutencao = :id_manutencao
                    """
            params = {
                'id_visita': manutencao_atualizada.get_visita().get_id_visita(),
                'id_acao': manutencao_atualizada.get_catalogo_acao().get_id_catalogo_acao(),
                'id_defeito': manutencao_atualizada.get_defeito().get_id_defeito(),
                'obs': manutencao_atualizada.get_obs_servico(),
                'id_manutencao': manutencao_atualizada.get_id_manutencao()
            }
            db.execute_write_query(query, params)
            print("Manutenção atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar manutenção: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_manutencao_em_empresa(self, id_empresa: int) -> list[Manutencao]:
        """ Lista todas as manutenções associadas a veículos de uma empresa específica. """
        db = OracleDB()
        lista_manutencoes = []
        try:
            db.connect()
            query = """
                    SELECT m.id_manutencao, m.obs_servico,
                           vt.id_visita, vt.data_visita,
                           ca.id_catalogo_acao, ca.codigo_acao, ca.descricao_acao,
                           d.id_defeito, d.data_reporte, d.status_defeito, d.obs_defeitos,
                           t.id_tecnico, t.local, t.status,
                           c.id_contato, c.nome_contato, c.email_contato, c.telefone,
                           cd.id_catalogo_defeito, cd.codigo_defeito, cd.descricao_defeito,
                           v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM manutenções m
                    JOIN visitas_tecnicas vt ON m.id_visita = vt.id_visita
                    JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                    JOIN contatos c ON t.id_contato = c.id_contato
                    JOIN catalogo_acoes ca ON m.id_catalogo_acao = ca.id_catalogo_acao
                    JOIN defeitos d ON m.id_defeito = d.id_defeito
                    JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    WHERE e.id_empresa = :id_empresa
                    ORDER BY vt.data_visita DESC
                    """
            resultado = db.execute_select(query, {'id_empresa': id_empresa})
            if resultado:
                for linha in resultado:
                    # Reconstrói todos os objetos aninhados a partir do resultado do JOIN
                    contato = Contato(id_contato=linha[14], nome_contato=linha[15], email_contato=linha[16],
                                      telefone=linha[17])
                    tecnico = Tecnico(id_tecnico=linha[11], local=linha[12], status=linha[13], contato=contato)
                    visita = VisitaTecnica(id_visita=linha[2], data_visita=linha[3], tecnico=tecnico)
                    catalogo_acao = CatalogoAcoes(id_catalogo_acao=linha[4], codigo_acao=linha[5],
                                                 descricao_acao=linha[6])
                    catalogo_defeito = CatalogoDefeitos(id_catalogo_defeito=linha[18], codigo_defeito=linha[19],
                                                       descricao_defeito=linha[20])
                    empresa = Empresa(id_empresa=linha[24], nome_fantasia=linha[25], endereco=linha[26])
                    veiculo = Veiculo(id_veiculo=linha[21], placa=linha[22], frota=linha[23], empresa=empresa)
                    defeito = Defeito(id_defeito=linha[7], data_reporte=linha[8], status_defeito=linha[9],
                                      obs_defeitos=linha[10], catalogo_defeito=catalogo_defeito, veiculo=veiculo)
                    manutencao = Manutencao(id_manutencao=linha[0], obs_servico=linha[1], visita=visita,
                                            catalogo_acao=catalogo_acao, defeito=defeito)
                    lista_manutencoes.append(manutencao)
            return lista_manutencoes
        except Exception as e:
            print(f"Erro ao listar manutenções da empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def listar_manutencao_em_veiculo(self, id_veiculo: int) -> list[Manutencao]:
        """ Lista todas as manutenções realizadas em um veículo específico. """
        db = OracleDB()
        lista_manutencoes = []
        try:
            db.connect()
            query = """
                    SELECT m.id_manutencao, m.obs_servico,
                           vt.id_visita, vt.data_visita,
                           ca.id_catalogo_acao, ca.codigo_acao, ca.descricao_acao,
                           d.id_defeito, d.data_reporte, d.status_defeito, d.obs_defeitos,
                           t.id_tecnico, t.local, t.status,
                           c.id_contato, c.nome_contato, c.email_contato, c.telefone,
                           cd.id_catalogo_defeito, cd.codigo_defeito, cd.descricao_defeito,
                           v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco
                    FROM manutenções m
                    JOIN visitas_tecnicas vt ON m.id_visita = vt.id_visita
                    JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                    JOIN contatos c ON t.id_contato = c.id_contato
                    JOIN catalogo_acoes ca ON m.id_catalogo_acao = ca.id_catalogo_acao
                    JOIN defeitos d ON m.id_defeito = d.id_defeito
                    JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    WHERE v.id_veiculo = :id_veiculo
                    ORDER BY vt.data_visita DESC
                    """
            resultado = db.execute_select(query, {'id_veiculo': id_veiculo})
            if resultado:
                for linha in resultado:
                    # A ordem das colunas é a mesma da query anterior
                    contato = Contato(id_contato=linha[14], nome_contato=linha[15], email_contato=linha[16],
                                      telefone=linha[17])
                    tecnico = Tecnico(id_tecnico=linha[11], local=linha[12], status=linha[13], contato=contato)
                    visita = VisitaTecnica(id_visita=linha[2], data_visita=linha[3], tecnico=tecnico)
                    catalogo_acao = CatalogoAcoes(id_catalogo_acao=linha[4], codigo_acao=linha[5],
                                                 descricao_acao=linha[6])
                    catalogo_defeito = CatalogoDefeitos(id_catalogo_defeito=linha[18], codigo_defeito=linha[19],
                                                       descricao_defeito=linha[20])
                    empresa = Empresa(id_empresa=linha[24], nome_fantasia=linha[25], endereco=linha[26])
                    veiculo = Veiculo(id_veiculo=linha[21], placa=linha[22], frota=linha[23], empresa=empresa)
                    defeito = Defeito(id_defeito=linha[7], data_reporte=linha[8], status_defeito=linha[9],
                                      obs_defeitos=linha[10], catalogo_defeito=catalogo_defeito, veiculo=veiculo)
                    manutencao = Manutencao(id_manutencao=linha[0], obs_servico=linha[1], visita=visita,
                                            catalogo_acao=catalogo_acao, defeito=defeito)
                    lista_manutencoes.append(manutencao)
            return lista_manutencoes
        except Exception as e:
            print(f"Erro ao listar manutenções do veículo: {e}")
            return []
        finally:
            if db.connection:
                db.close()