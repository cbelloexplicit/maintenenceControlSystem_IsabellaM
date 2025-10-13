from src.conexion.OracleDB import OracleDB
import os

def executar_script_sql(caminho_script: str):
    # Lê um arquivo .sql e cria a estrutura do banco.
    db = OracleDB()
    try:
        print(f"Lendo o script SQL em: {caminho_script}")
        with open(caminho_script, 'r', encoding='utf-8') as f:
            script_completo = f.read()
        comandos_sql = script_completo.split(';')

        # Conecta ao banco de dados
        if db.connect():
            print("Executando comandos SQL...")
            for comando in comandos_sql:
                # Ignora comandos vazios ';')
                if comando.strip():
                    db.cursor.execute(comando)

            # Salva alterações
            db.connection.commit()
            print("Script SQL executado com sucesso! Tabelas e sequences foram criadas.")

    except FileNotFoundError:
        print(f"ERRO: Arquivo de script não encontrado em '{caminho_script}'. Verifique o caminho.")
    except Exception as e:
        print(f"ERRO ao executar o script SQL: {e}")
        if db.connection:
            db.connection.rollback() # Reverte alterações em caso de erro
    finally:
        if db.connection:
            db.disconnect() # Garante que a conexão seja sempre fechada

# --- Ponto de Entrada do Script ---
if __name__ == '__main__':
    caminho_do_script = os.path.join("sql", "main.sql")

    executar_script_sql(caminho_do_script)