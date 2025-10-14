from src.conexion.oracledb import OracleDB
from src.model.empresa import Empresa
from src.model.veiculo import Veiculo
from src.model.contato import Contato
from src.model.tecnico import Tecnico

# o programa no main deve conferir o ID da modificação, exclusão, etc
#antes de realizar qualquer alteração ou liberar informações
class Controller_Empresa:
    def __init__(self):
        pass

    def inserir_empresa(self, nova_empresa: Empresa) -> bool:
        """ Insere uma nova empresa no banco de dados. """
        #NO MAIN, O PROGRAMA DEVE CONFERIR COM O USUARIO SE A EMPRESA JA NAO EXISTE NO BD ANTES DE INSERIR
        #REALIZA LISTAGEM POR NOME, CONFERE, ENTAO INSERE
        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO empresas (id_empresa, nome_fantasia, endereco) 
                    VALUES (seq_empresas.nextval, :nome, :endereco)
                    """
            params = {
                'nome': nova_empresa.get_nome_fantasia(),
                'endereco': nova_empresa.get_endereco()
            }
            db.execute_write_query(query, params)
            print("Empresa inserida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir empresa: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_empresa(self, id_empresa: int) -> bool:
        """ Remove uma empresa do banco, após verificar dependências. """
        db = OracleDB()
        try:
            db.connect()
            # Verifica se a empresa está sendo usada em outras tabelas
            tabelas_dependentes = ["USUARIOS", "VEICULOS", "EMPRESA_CONTATOS", "TECNICOS_EMPRESAS", "LOG_LOT"]
            for tabela in tabelas_dependentes:
                query_check = f"SELECT 1 FROM {tabela} WHERE id_empresa = :id_empresa"
                if db.cursor.execute(query_check, {'id_empresa': id_empresa}).fetchone():
                    print(
                        f"Erro: Não é possível remover a empresa (ID: {id_empresa}), pois ela está em uso na tabela '{tabela}'.")
                    return False

            # Se não houver dependências, remove a empresa
            query_delete = "DELETE FROM empresas WHERE id_empresa = :id_empresa"
            db.execute_write_query(query_delete, {'id_empresa': id_empresa})
            print(f"Empresa (ID: {id_empresa}) removida com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover empresa: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_empresa(self, empresa_atualizada: Empresa) -> bool:
        """ Atualiza os dados de uma empresa existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE empresas
                    SET nome_fantasia = :nome, endereco = :endereco
                    WHERE id_empresa = :id_empresa
                    """
            params = {
                'nome': empresa_atualizada.get_nome_fantasia(),
                'endereco': empresa_atualizada.get_endereco(),
                'id_empresa': empresa_atualizada.get_id_empresa()
            }
            db.execute_write_query(query, params)
            print("Empresa atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar empresa: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_empresas(self) -> list[Empresa]:
        """ Lista todas as empresas cadastradas. """
        db = OracleDB()
        lista_empresas = []
        try:
            db.connect()
            query = "SELECT id_empresa, nome_fantasia, endereco FROM empresas ORDER BY nome_fantasia"
            resultado = db.execute_select(query)
            if resultado:
                for linha in resultado:
                    empresa = Empresa(id_empresa=linha[0], nome_fantasia=linha[1], endereco=linha[2])
                    lista_empresas.append(empresa)
            return lista_empresas
        except Exception as e:
            print(f"Erro ao listar empresas: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_empresa_por_nome(self, nome: str) -> list[Empresa]:
        """ Busca empresas cujo nome fantasia contenha o texto fornecido. """
        db = OracleDB()
        lista_empresas = []
        try:
            db.connect()
            query = """
                    SELECT id_empresa, nome_fantasia, endereco FROM empresas 
                    WHERE UPPER(nome_fantasia) LIKE UPPER(:nome_param)
                    ORDER BY nome_fantasia
                    """
            params = {'nome_param': f'%{nome}%'}
            resultado = db.execute_select(query, params)
            if resultado:
                for linha in resultado:
                    empresa = Empresa(id_empresa=linha[0], nome_fantasia=linha[1], endereco=linha[2])
                    lista_empresas.append(empresa)
            return lista_empresas
        except Exception as e:
            print(f"Erro ao buscar empresas por nome: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def listar_veiculos_em_empresa(self, id_empresa: int) -> list[Veiculo]:
        """ Lista todos os veículos associados a uma empresa específica. """
        db = OracleDB()
        lista_veiculos = []
        try:
            db.connect()
            # Primeiro, busca os dados da empresa para reconstruir o objeto
            query_empresa = "SELECT id_empresa, nome_fantasia, endereco FROM empresas WHERE id_empresa = :id_empresa"
            resultado_empresa = db.execute_select(query_empresa, {'id_empresa': id_empresa})
            if not resultado_empresa:
                print(f"Empresa com ID {id_empresa} não encontrada.")
                return []

            empresa_obj = Empresa(id_empresa=resultado_empresa[0][0], nome_fantasia=resultado_empresa[0][1],
                                  endereco=resultado_empresa[0][2])

            # Agora, busca os veículos dessa empresa
            query_veiculos = "SELECT id_veiculo, placa, frota FROM veiculos WHERE id_empresa = :id_empresa ORDER BY placa"
            resultado_veiculos = db.execute_select(query_veiculos, {'id_empresa': id_empresa})

            if resultado_veiculos:
                for linha in resultado_veiculos:
                    veiculo = Veiculo(id_veiculo=linha[0], placa=linha[1], frota=linha[2], empresa=empresa_obj)
                    lista_veiculos.append(veiculo)
            return lista_veiculos
        except Exception as e:
            print(f"Erro ao listar veículos da empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def listar_contatos_da_empresa(self, id_empresa: int) -> list[Contato]:
        """ Lista todos os contatos associados a uma empresa específica. """
        db = OracleDB()
        lista_contatos = []
        try:
            db.connect()
            query = """
                        SELECT c.id_contato, c.nome_contato, c.email_contato, c.telefone 
                        FROM contatos c
                        JOIN empresa_contatos ec ON c.id_contato = ec.id_contato
                        WHERE ec.id_empresa = :id_empresa
                        ORDER BY c.nome_contato
                        """
            resultado = db.execute_select(query, {'id_empresa': id_empresa})
            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[0], nome_contato=linha[1], email_contato=linha[2],
                                      telefone=linha[3])
                    lista_contatos.append(contato)
            return lista_contatos
        except Exception as e:
            print(f"Erro ao listar contatos da empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def listar_tecnicos_em_empresa(self, id_empresa: int) -> list[Tecnico]:
        """ Lista todos os técnicos associados a uma empresa específica. """
        db = OracleDB()
        lista_tecnicos = []
        try:
            db.connect()
            query = """
                        SELECT t.id_tecnico, t.local, 
                               c.id_contato, c.nome_contato, c.email_contato, c.telefone
                        FROM tecnicos t
                        JOIN tecnicos_empresas te ON t.id_tecnico = te.id_tecnico
                        JOIN contatos c ON t.id_contato = c.id_contato
                        WHERE te.id_empresa = :id_empresa
                        ORDER BY c.nome_contato
                        """
            resultado = db.execute_select(query, {'id_empresa': id_empresa})
            if resultado:
                for linha in resultado:
                    contato = Contato(id_contato=linha[2], nome_contato=linha[3], email_contato=linha[4],
                                      telefone=linha[5])
                    tecnico = Tecnico(id_tecnico=linha[0], local=linha[1], contato=contato)
                    lista_tecnicos.append(tecnico)
            return lista_tecnicos
        except Exception as e:
            print(f"Erro ao listar técnicos da empresa: {e}")
            return []
        finally:
            if db.connection:
                db.close()