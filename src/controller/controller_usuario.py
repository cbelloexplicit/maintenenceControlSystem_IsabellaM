from src.conexion.oracledb import OracleDB
from src.model.usuario import Usuario

class ControllerUsuario:

    def inserir_usuario(self, novo_usuario: Usuario) -> None:
        """
        Insere um novo usuário no banco de dados.
        """
        db = OracleDB()
        try:
            db.connect()
            
            # Monta a query de inserção usando a SEQUENCE para gerar o ID
            query = """
                    INSERT INTO usuarios (id_usuario, nome_completo, email_usuario, senha_hash) 
                    VALUES (seq_usuarios.nextval, :nome, :email, :senha)
                    """
            params = {
                'nome': novo_usuario.get_nome_completo(),
                'email': novo_usuario.get_email_usuario(),
                'senha': novo_usuario.get_senha_hash()
            }
            db.execute_query(query, params)
            print("Usuário inserido com sucesso!")

        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
        finally:
            if db.connection:
                db.close()

    # Aqui você implementará os outros métodos: listar_usuarios, atualizar_usuario, etc.
