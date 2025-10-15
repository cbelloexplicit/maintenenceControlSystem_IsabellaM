from src.conexion.oracledb import OracleDB
from src.model.catalogo_eventos import CatalogoEventos


class Controller_Catalogo_Eventos:

    def __init__(self):
        pass

    def inserir_evento(self, novo_evento: CatalogoEventos) -> bool:
        """ Insere um novo tipo de evento no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o código do evento já existe para evitar duplicatas
            if self.buscar_evento_por_codigo(novo_evento.get_codigo_evento()):
                print(f"Erro ao inserir: O código de evento '{novo_evento.get_codigo_evento()}' já existe.")
                return False

            query = """
                    INSERT INTO catalogo_eventos (id_catalogo_eventos, codigo_evento) 
                    VALUES (seq_catalogo_eventos.nextval, :codigo)
                    """
            params = {'codigo': novo_evento.get_codigo_evento()}
            db.execute_write_query(query, params)
            print("Evento do catálogo inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir evento no catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_evento(self, id_catalogo_eventos: int) -> bool:
        """ Remove um evento do catálogo, após verificar se ele não está em uso. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se o evento está sendo usado na tabela de LOG_LOT
            query_check = "SELECT 1 FROM LOG_LOT WHERE id_catalogo_eventos = :id_evento"
            if db.cursor.execute(query_check, {'id_evento': id_catalogo_eventos}).fetchone():
                print(
                    f"Erro: Não é possível remover o evento (ID: {id_catalogo_eventos}), pois ele está em uso no histórico de lotes.")
                return False

            query_delete = "DELETE FROM catalogo_eventos WHERE id_catalogo_eventos = :id_evento"
            db.execute_write_query(query_delete, {'id_evento': id_catalogo_eventos})
            print(f"Evento do catálogo (ID: {id_catalogo_eventos}) removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover evento do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_evento(self, evento_atualizado: CatalogoEventos) -> bool:
        """ Atualiza os dados de um evento existente no catálogo. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE catalogo_eventos
                    SET codigo_evento = :codigo
                    WHERE id_catalogo_eventos = :id_evento
                    """
            params = {
                'codigo': evento_atualizado.get_codigo_evento(),
                'id_evento': evento_atualizado.get_id_catalogo_eventos()
            }
            db.execute_write_query(query, params)
            print("Evento do catálogo atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar evento do catálogo: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_eventos(self) -> list[CatalogoEventos]:
        """ Lista todos os eventos do catálogo. """
        db = OracleDB()
        lista_eventos = []
        try:
            db.connect()
            query = "SELECT id_catalogo_eventos, codigo_evento FROM catalogo_eventos ORDER BY codigo_evento"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    evento = CatalogoEventos(id_catalogo_eventos=linha[0], codigo_evento=linha[1])
                    lista_eventos.append(evento)
            return lista_eventos
        except Exception as e:
            print(f"Erro ao listar eventos do catálogo: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_evento_por_codigo(self, codigo_evento: str) -> CatalogoEventos | None:
        """ Busca um evento específico no catálogo pelo seu código (case-insensitive). """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT id_catalogo_eventos, codigo_evento FROM catalogo_eventos 
                    WHERE UPPER(codigo_evento) = UPPER(:codigo)
                    """
            params = {'codigo': codigo_evento}
            resultado = db.execute_select(query, params)
            if resultado:
                linha = resultado[0]
                evento = CatalogoEventos(id_catalogo_eventos=linha[0], codigo_evento=linha[1])
                return evento
            return None
        except Exception as e:
            print(f"Erro ao buscar evento por código: {e}")
            return None
        finally:
            if db.connection:
                db.close()