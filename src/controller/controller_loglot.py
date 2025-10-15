from src.conexion.oracledb import OracleDB
from src.model.log_lot import LogLot
from src.model.lot import Lot
from src.model.veiculo import Veiculo
from src.model.empresa import Empresa
from src.model.manutencao import Manutencao
from src.model.catalogo_eventos import CatalogoEventos


class Controller_LogLot:

    def __init__(self):
        pass

    def inserir_log(self, novo_log: LogLot) -> bool:
        """
        Insere um novo registro de evento (log) no histórico de um lote.
        Lida com campos opcionais (id_veiculo, id_empresa, id_manutencao).
        """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO log_lot (id_log, id_lot, id_veiculo, id_empresa, id_manutencao, 
                                         id_catalogo_eventos, data_evento, responsavel_evento, obs_evento) 
                    VALUES (seq_log_lot.nextval, :id_lot, :id_veiculo, :id_empresa, :id_manutencao, 
                            :id_catalogo, :data_evento, :responsavel, :obs)
                    """

            # Prepara os parâmetros, lidando com os objetos que podem ser Nulos
            params = {
                'id_lot': novo_log.get_lote().get_id_lot(),
                'id_veiculo': novo_log.get_veiculo().get_id_veiculo() if novo_log.get_veiculo() else None,
                'id_empresa': novo_log.get_empresa().get_id_empresa() if novo_log.get_empresa() else None,
                'id_manutencao': novo_log.get_manutencao().get_id_manutencao() if novo_log.get_manutencao() else None,
                'id_catalogo': novo_log.get_catalogo_eventos().get_id_catalogo_eventos(),
                'data_evento': novo_log.get_data_evento(),
                'responsavel': novo_log.get_responsavel_evento(),
                'obs': novo_log.get_obs_evento()
            }

            db.execute_write_query(query, params)
            print("Log de evento inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir log de evento: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_log_por_lot(self, id_lot: int) -> list[LogLot]:
        """
        Busca e lista o histórico completo de eventos para um lote (dispositivo) específico.
        Funciona como o "buscar log por lot".
        """
        db = OracleDB()
        lista_logs = []
        try:
            db.connect()
            # Query complexa com LEFT JOIN para buscar todos os dados, mesmo os opcionais
            query = """
                    SELECT ll.id_log, ll.data_evento, ll.responsavel_evento, ll.obs_evento,
                           l.id_lot, l.codigo_lot, l.obs_lot,
                           ce.id_catalogo_eventos, ce.codigo_evento,
                           v.id_veiculo, v.placa, v.frota,
                           e.id_empresa, e.nome_fantasia, e.endereco,
                           m.id_manutencao, m.obs_servico
                    FROM log_lot ll
                    INNER JOIN lots l ON ll.id_lot = l.id_lot
                    INNER JOIN catalogo_eventos ce ON ll.id_catalogo_eventos = ce.id_catalogo_eventos
                    LEFT JOIN veiculos v ON ll.id_veiculo = v.id_veiculo
                    LEFT JOIN empresas e ON ll.id_empresa = e.id_empresa
                    LEFT JOIN manutenções m ON ll.id_manutencao = m.id_manutencao
                    WHERE ll.id_lot = :id_lot
                    ORDER BY ll.data_evento DESC
                    """

            resultado = db.execute_select(query, {'id_lot': id_lot})

            if resultado:
                for linha in resultado:
                    # Reconstrói os objetos a partir do resultado do JOIN.
                    # É preciso verificar se os dados opcionais (veiculo, empresa, etc.) não são nulos.

                    lote = Lot(id_lot=linha[4], codigo_lot=linha[5], obs_lot=linha[6])
                    catalogo_evento = CatalogoEventos(id_catalogo_eventos=linha[7], codigo_evento=linha[8])

                    veiculo = None
                    if linha[9] is not None:
                        # Para reconstruir o Veiculo, precisaríamos de mais um JOIN para a Empresa do Veiculo.
                        # Para simplificar, vamos criar um objeto Veiculo parcial.
                        veiculo = Veiculo(id_veiculo=linha[9], placa=linha[10], frota=linha[11], empresa=None)

                    empresa = None
                    if linha[12] is not None:
                        empresa = Empresa(id_empresa=linha[12], nome_fantasia=linha[13], endereco=linha[14])

                    manutencao = None
                    if linha[15] is not None:
                        # Para reconstruir a Manutencao, precisaríamos de muitos JOINs.
                        # Para simplificar, criamos um objeto Manutencao parcial.
                        manutencao = Manutencao(id_manutencao=linha[15], obs_servico=linha[16], visita=None,
                                                catalogo_acao=None, defeito=None)

                    log_evento = LogLot(id_log=linha[0], data_evento=linha[1], responsavel_evento=linha[2],
                                         obs_evento=linha[3],
                                         lote=lote, catalogo_eventos=catalogo_evento, veiculo=veiculo,
                                         empresa=empresa, manutencao=manutencao)

                    lista_logs.append(log_evento)

            return lista_logs
        except Exception as e:
            print(f"Erro ao listar o histórico do lote: {e}")
            return []
        finally:
            if db.connection:
                db.close()