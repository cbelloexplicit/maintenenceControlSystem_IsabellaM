# Arquivo: src/controller/controller_usuario.py

from src.conexion.oracledb import OracleDB
from src.model.usuario import Usuario
import hashlib


class ControllerUsuario:
    def __init__(self):
        pass

    def inserir_usuario(self, novo_usuario: Usuario) -> bool:
        """ Insere um novo usuário no banco de dados. """
        if self.buscar_usuario_por_email(novo_usuario.get_email_usuario()):
            print(f"Erro ao inserir: O e-mail '{novo_usuario.get_email_usuario()}' já está cadastrado.")
            return False

        db = OracleDB()
        try:
            db.connect()
            query = """
                    INSERT INTO usuarios (id_usuario, nome_completo, email_usuario, senha_hash) 
                    VALUES (seq_usuarios.nextval, :nome, :email, :senha)
                    """
            params = {
                'nome': novo_usuario.get_nome_completo(),
                'email': novo_usuario.get_email_usuario(),
                'senha': novo_usuario.get_senha_hash()
            }
            db.execute_write_query(query, params)
            print("Usuário inserido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def remover_usuario(self, id_usuario: int) -> bool:
        """ Remove um usuário do banco de dados pelo seu ID. """
        db = OracleDB()
        try:
            db.connect()
            query = "DELETE FROM usuarios WHERE id_usuario = :id_usuario"
            params = {'id_usuario': id_usuario}
            db.execute_write_query(query, params)
            print(f"Usuário ID {id_usuario} removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover usuário: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def atualizar_usuario(self, usuario_atualizado: Usuario) -> bool:
        """ Atualiza os dados de um usuário existente. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    UPDATE usuarios
                    SET nome_completo = :nome, email_usuario = :email, senha_hash = :senha_hash
                    WHERE id_usuario = :id_usuario
                    """
            params = {
                'nome': usuario_atualizado.get_nome_completo(),
                'email': usuario_atualizado.get_email_usuario(),
                'senha_hash': usuario_atualizado.get_senha_hash(),
                'id_usuario': usuario_atualizado.get_id_usuario()
            }
            db.execute_write_query(query, params)
            print("Usuário atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False
        finally:
            if db.connection:
                db.close()

    def listar_todos_usuarios(self) -> list[Usuario]:
        """ Lista todos os usuários cadastrados. """
        db = OracleDB()
        lista_de_usuarios = []
        try:
            db.connect()
            query = "SELECT id_usuario, nome_completo, email_usuario, senha_hash FROM usuarios ORDER BY nome_completo"
            resultado_bruto = db.execute_select(query)
            if resultado_bruto:
                for linha in resultado_bruto:
                    usuario = Usuario(id_usuario=linha[0], nome_completo=linha[1], email_usuario=linha[2],
                                      senha_hash=linha[3])
                    lista_de_usuarios.append(usuario)
            return lista_de_usuarios
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def buscar_usuario_por_nome(self, nome: str) -> list[Usuario]:
        """ Busca usuários cujo nome contenha o texto fornecido. """
        db = OracleDB()
        lista_de_usuarios = []
        try:
            db.connect()
            query = """
                    SELECT id_usuario, nome_completo, email_usuario, senha_hash FROM usuarios 
                    WHERE UPPER(nome_completo) LIKE UPPER(:nome_param)
                    ORDER BY nome_completo
                    """
            params = {'nome_param': f'%{nome}%'}
            resultado = db.execute_select(query, params)
            if resultado:
                for linha in resultado:
                    usuario = Usuario(id_usuario=linha[0], nome_completo=linha[1], email_usuario=linha[2],
                                      senha_hash=linha[3])
                    lista_de_usuarios.append(usuario)
            return lista_de_usuarios
        except Exception as e:
            print(f"Erro ao buscar usuários por nome: {e}")
            return []
        finally:
            if db.connection:
                db.close()

    def validar_login(self, email: str, senha: str) -> Usuario | None:
        """ Valida as credenciais de um usuário para login (case-insensitive). """
        usuario_encontrado = self.buscar_usuario_por_email(email)

        if not usuario_encontrado:
            print(f"Login falhou: E-mail '{email}' não encontrado.")
            return None

        senha_hash_armazenada = usuario_encontrado.get_senha_hash()
        senha_fornecida_hash = hashlib.sha256(senha.encode()).hexdigest()

        if senha_fornecida_hash == senha_hash_armazenada:
            print("Login bem-sucedido!")
            return usuario_encontrado
        else:
            print("Login falhou: Senha incorreta.")
            return None

    def buscar_usuario_por_email(self, email: str) -> Usuario | None:
        """ Busca um usuário pelo e-mail exato, de forma case-insensitive. """
        db = OracleDB()
        try:
            db.connect()
            query = """
                    SELECT id_usuario, nome_completo, email_usuario, senha_hash 
                    FROM usuarios 
                    WHERE UPPER(email_usuario) = UPPER(:email_param)
                    """
            params = {'email_param': email}
            resultado = db.execute_select(query, params)

            if resultado:
                linha = resultado[0]
                usuario_encontrado = Usuario(id_usuario=linha[0], nome_completo=linha[1], email_usuario=linha[2],
                                             senha_hash=linha[3])
                return usuario_encontrado
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por e-mail: {e}")
            return None
        finally:
            if db.connection:
                db.close()