from src.conexion.oracledb import OracleDB

class Relatorios:
    def __init__(self):
        pass

    def get_relatorio_atividades_tecnico(self, id_tecnico: int) -> list[dict]:
        """
        Gera um relatório detalhado de todas as atividades de um técnico específico.
        """
        db = OracleDB()
        relatorio = []
        try:
            db.connect()
            query = """
                    SELECT 
                        vt.data_visita,
                        v.placa as veiculo_placa,
                        cd.descricao_defeito as defeito_reportado,
                        ca.descricao_acao as acao_realizada,
                        m.obs_servico
                    FROM visitas_tecnicas vt
                    JOIN manutenções m ON vt.id_visita = m.id_visita
                    JOIN defeitos d ON m.id_defeito = d.id_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                    JOIN catalogo_acoes ca ON m.id_catalogo_acao = ca.id_catalogo_acao
                    WHERE vt.id_tecnico = :id_tecnico
                    ORDER BY vt.data_visita DESC
                    """

            resultado = db.execute_select(query, {'id_tecnico': id_tecnico})

            if resultado:
                for linha in resultado:
                    relatorio.append({
                        "data_visita": linha[0],
                        "veiculo_placa": linha[1],
                        "defeito_reportado": linha[2],
                        "acao_realizada": linha[3],
                        "observacao": linha[4]
                    })

            return relatorio
        except Exception as e:
            print(f"Erro ao gerar relatório do técnico: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def get_relatorio_manutencoes_por_empresa(self) -> list[dict]:
        """
        Gera um relatório com a contagem de manutenções realizadas por empresa.
        """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT 
                        e.nome_fantasia, 
                        COUNT(m.id_manutencao) as total_manutencoes
                    FROM manutenções m
                    JOIN defeitos d ON m.id_defeito = d.id_defeito
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    GROUP BY e.nome_fantasia
                    ORDER BY total_manutencoes DESC
                    """
            resultado = db.execute_select(query)
            return [{'empresa': linha[0], 'total_manutencoes': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório de manutenções por empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def get_relatorio_defeitos_por_empresa(self) -> list[dict]:
        """
        Gera um relatório com a contagem de defeitos reportados por empresa.
        """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT 
                        e.nome_fantasia, 
                        COUNT(d.id_defeito) as total_defeitos
                    FROM defeitos d
                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                    JOIN empresas e ON v.id_empresa = e.id_empresa
                    GROUP BY e.nome_fantasia
                    ORDER BY total_defeitos DESC
                    """
            resultado = db.execute_select(query)
            return [{'empresa': linha[0], 'total_defeitos': linha[1]} for linha in resultado]
        except Exception as e:
            print(f"Erro ao gerar relatório de defeitos por empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def get_relatorio_detalhado_empresa(self, id_empresa: int) -> dict:
        """
        Gera um relatório detalhado para uma empresa, incluindo veículos,
        técnicos, histórico de manutenções e defeitos atuais.
        """
        db = OracleDB()
        relatorio_completo = {
            "veiculos": [],
            "tecnicos": [],
            "manutencoes": [],
            "defeitos_atuais": []
        }
        try:
            db.connect()

            # 1. Busca os veículos da empresa
            query_veiculos = "SELECT placa, frota FROM veiculos WHERE id_empresa = :id_empresa ORDER BY placa"
            resultado_veiculos = db.execute_select(query_veiculos, {'id_empresa': id_empresa})
            if resultado_veiculos:
                relatorio_completo["veiculos"] = [{"placa": v[0], "frota": v[1]} for v in resultado_veiculos]

            # 2. Busca os técnicos associados à empresa
            query_tecnicos = """
                             SELECT c.nome_contato, t.local FROM tecnicos t
                             JOIN contatos c ON t.id_contato = c.id_contato
                             JOIN tecnicos_empresas te ON t.id_tecnico = te.id_tecnico
                             WHERE te.id_empresa = :id_empresa ORDER BY c.nome_contato
                             """
            resultado_tecnicos = db.execute_select(query_tecnicos, {'id_empresa': id_empresa})
            if resultado_tecnicos:
                relatorio_completo["tecnicos"] = [{"nome": t[0], "local": t[1]} for t in resultado_tecnicos]

            # 3. Busca o histórico de manutenções
            query_manutencoes = """
                                SELECT vt.data_visita, v.placa, cd.descricao_defeito, ca.descricao_acao, c.nome_contato as nome_tecnico
                                FROM manutenções m
                                JOIN defeitos d ON m.id_defeito = d.id_defeito
                                JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                                JOIN visitas_tecnicas vt ON m.id_visita = vt.id_visita
                                JOIN tecnicos t ON vt.id_tecnico = t.id_tecnico
                                JOIN contatos c ON t.id_contato = c.id_contato
                                JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                                JOIN catalogo_acoes ca ON m.id_catalogo_acao = ca.id_catalogo_acao
                                WHERE v.id_empresa = :id_empresa
                                ORDER BY vt.data_visita DESC
                                """
            resultado_manutencoes = db.execute_select(query_manutencoes, {'id_empresa': id_empresa})
            if resultado_manutencoes:
                for m in resultado_manutencoes:
                    relatorio_completo["manutencoes"].append({
                        "data": m[0], "placa": m[1], "defeito": m[2], "acao": m[3], "tecnico": m[4]
                    })

            # 4. NOVA CONSULTA: Busca os defeitos com status 'ATIVO'
            query_defeitos_atuais = """
                                    SELECT v.placa, d.data_reporte, cd.descricao_defeito, d.status_defeito
                                    FROM defeitos d
                                    JOIN veiculos v ON d.id_veiculo = v.id_veiculo
                                    JOIN catalogo_defeitos cd ON d.id_catalogo_defeito = cd.id_catalogo_defeito
                                    WHERE v.id_empresa = :id_empresa AND d.status_defeito = 'ATIVO'
                                    ORDER BY d.data_reporte ASC
                                    """
            resultado_defeitos = db.execute_select(query_defeitos_atuais, {'id_empresa': id_empresa})
            if resultado_defeitos:
                for d in resultado_defeitos:
                    relatorio_completo["defeitos_atuais"].append({
                        "placa": d[0], "data_reporte": d[1], "descricao": d[2], "status": d[3]
                    })

            return relatorio_completo
        except Exception as e:
            print(f"Erro ao gerar relatório detalhado da empresa: {e}")
            return relatorio_completo
        finally:
            if db.connection:
                db.close()