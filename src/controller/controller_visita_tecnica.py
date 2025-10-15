from src.conexion.oracledb import OracleDB
from src.model.visita_tecnica import VisitaTecnica
from src.model.tecnico import Tecnico
from src.model.contato import Contato
from datetime import date


class Controller_VisitaTecnica:

    def __init__(self):
        pass

    def inserir_visita(self, nova_visita: VisitaTecnica) -> bool:
        """ Insere uma nova visita técnica no banco de dados. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO visitas_tecnicas (id_visita, id_tecnico, data_visita) 
                    VALUES (seq_visitas_tecnicas.nextval, :id_tecnico, :data_visita)
                    """
            params = {
                'id_tecnico': nova_visita.get_tecnico().get_id_tecnico(),
                'data_visita': nova_visita.get_data_visita()
            }
            db.execute_write_query(query, params)
            print("Visita técnica inserida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir visita técnica: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_visita(self, id_visita: int) -> bool:
        """ Remove uma visita técnica do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            query_check = "SELECT 1 FROM MANUTENCOES WHERE id_visita = :id_visita"
            if db.cursor.execute(query_check, {'id_visita': id_visita}).fetchone():
                print(
                    f"Erro: Não é possível remover a visita (ID: {id_visita}), pois ela possui manutenções associadas.")
                return False

            query_delete = "DELETE FROM visitas_tecnicas WHERE id_visita = :id_visita"
            db.execute_write_query(query_delete, {'id_visita': id_visita})
            print(f"Visita técnica (ID: {id_visita}) removida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover visita técnica: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_visita(self, visita_atualizada: VisitaTecnica) -> bool:
        """ Atualiza os dados de uma visita técnica existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE visitas_tecnicas
                    SET id_tecnico = :id_tecnico, data_visita = :data_visita
                    WHERE id_visita = :id_visita
                    """
            params = {
                'id_tecnico': visita_atualizada.get_tecnico().get_id_tecnico(),
                'data_visita': visita_atualizada.get_data_visita(),
                'id_visita': visita_atualizada.get_id_visita()
            }
            db.execute_write_query(query, params)
            print("Visita técnica atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar visita técnica: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_tudo(self) -> list[VisitaTecnica]:
        """ Lista todas as visitas técnicas cadastradas. """
        return self._executar_busca()

    def buscar_visita_por_data(self, data: date) -> list[VisitaTecnica]:
        """ Busca visitas técnicas que ocorreram em uma data específica. """
        where_clause = "WHERE TRUNC(vt.data_visita) = TRUNC(:param)"
        return self._executar_busca(where_clause, {'param': data})

    def buscar_visita_por_tecnico(self, id_tecnico: int) -> list[VisitaTecnica]:
        """ Busca todas as visitas realizadas por um técnico específico. """
        where_clause = "WHERE vt.id_tecnico = :param"
        return self._executar_busca(where_clause, {'param': id_tecnico})

    def buscar_visita_por_empresa(self, id_empresa: int) -> list[VisitaTecnica]:
        """ Busca todas as visitas associadas a uma empresa (via técnico). """
        join_clause = "JOIN tecnicos_empresas te ON t.id_tecnico = te.id_tecnico"
        where_clause = "WHERE te.id_empresa = :param"
        return self._executar_busca(where_clause, {'param': id_empresa}, join_clause)

    def buscar_visita_por_veiculo(self, id_veiculo: int) -> list[VisitaTecnica]:
        """ Busca todas as visitas que tiveram manutenções em um veículo específico. """
        join_clause = """
                      JOIN manutenções m ON vt.id_visita = m.id_visita
                      JOIN defeitos d ON m.id_defeito = d.id_defeito
                      """
        where_clause = "WHERE d.id_veiculo = :param"
        return self._executar_busca(where_clause, {'param': id_veiculo}, join_clause, distinct=True)

    def _executar_busca(self, where_clause: str = "", params: dict = None, join_clause: str = "",
                        distinct: bool = False) -> list[VisitaTecnica]:
        """ auxiliar genérico para executar as buscas de visitas. """
        db = OracleDB()
        lista_visitas = []
        try:
            db.connect()
            distinct_str = "DISTINCT" if distinct else ""
            query = f"""
                    SELECT {distinct_str} vt.id_visita, vt.data_visita,
                           t.id_tecnico, t.local, t.status,
                           c.id_contato, c.nome_contato, c.email_contato, c.telefone
                    FROM visitas_tecnicas vt
                    JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                    JOIN contatos c ON t.id_contato = c.id_contato
                    {join_clause}
                    {where_clause}
                    ORDER BY vt.data_visita DESC
                    """
            resultado = db.execute_select(query, params or {})
            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[5], nome_contato=linha[6], email_contato=linha[7],
                                      telefone=linha[8])
                    tecnico = Tecnico(id_tecnico=linha[2], local=linha[3], status=linha[4], contato=contato)
                    visita = VisitaTecnica(id_visita=linha[0], data_visita=linha[1], tecnico=tecnico)
                    lista_visitas.append(visita)
            return lista_visitas
        except Exception as e:
            print(f"Erro ao buscar visitas: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def relatorio_contagem_visitas_por_tecnico(self) -> list[dict]:
        """ Gera um relatório com a contagem de visitas por técnico. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT c.nome_contato, COUNT(vt.id_visita) as total_visitas
                    FROM visitas_tecnicas vt
                    JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                    JOIN contatos c ON t.id_contato = c.id_contato
                    GROUP BY c.nome_contato
                    ORDER BY total_visitas DESC
                    """
            resultado = db.execute_select(query)
            return [{'tecnico': linha[0], 'total_visitas': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório por técnico: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def relatorio_contagem_visitas_por_empresa(self) -> list[dict]:
        """ Gera um relatório com a contagem de visitas por empresa. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT e.nome_fantasia, COUNT(vt.id_visita) as total_visitas
                    FROM visitas_tecnicas vt
                    JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                    JOIN tecnicos_empresas te ON t.id_tecnico = te.id_tecnico
                    JOIN empresas e ON te.id_empresa = e.id_empresa
                    GROUP BY e.nome_fantasia
                    ORDER BY total_visitas DESC
                    """
            resultado = db.execute_select(query)
            return [{'empresa': linha[0], 'total_visitas': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório por empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def relatorio_contagem_visitas_por_veiculo(self) -> list[dict]:
        """ Gera um relatório com a contagem de visitas por veículo. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT v.placa, COUNT(DISTINCT vt.id_visita) as total_visitas
                    FROM visitas_tecnicas vt
                    JOIN manutenções m ON vt.id_visita = m.id_visita
                    JOIN defeitos d ON m.id_defeito = d.id_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    GROUP BY v.placa
                    ORDER BY total_visitas DESC
                    """
            resultado = db.execute_select(query)
            return [{'veiculo_placa': linha[0], 'total_visitas': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório por veículo: {e}")
            return []
        finally:
            if db.connection:
                db.close()