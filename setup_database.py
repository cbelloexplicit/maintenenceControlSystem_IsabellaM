from src.conexion.OracleDB import OracleDB
import os
import re


def executar_script_sql(caminho_script: str):
    """
    Lê um arquivo .sql, **limpa os comentários** e executa seus comandos um por um.
    """
    db = OracleDB()

    try:
        print(f"Lendo o script SQL em: {caminho_script}")
        with open(caminho_script, 'r', encoding='utf-8') as f:
            script_completo = f.read()

        # Limpeza do Script
        # Remove comentários de linha (-- ...)
        script_limpo = re.sub(r'--.*?\n', ' ', script_completo)
        # Remove comentários de bloco (/* ... */)
        script_limpo = re.sub(r'/\*.*?\*/', ' ', script_limpo, flags=re.DOTALL)
        # Substitui quebras de linha e tabulações por espaços
        script_limpo = script_limpo.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # ------------------------------------

        # Divide o script limpo em comandos individuais
        comandos_sql = script_limpo.split(';')

        if db.connect():
            print("Executando comandos SQL...")
            for i, comando in enumerate(comandos_sql):
                comando_strip = comando.strip()
                if comando_strip:
                    try:
                        print(f"Executando comando {i + 1}...")
                        db.cursor.execute(comando_strip)
                    except Exception as e:
                        print(f"ERRO no comando: {comando_strip}")
                        raise e  # Levanta o erro para ser pego pelo bloco principal

            db.connection.commit()
            print("Script SQL executado com sucesso! Tabelas e sequences foram criadas.")

    except FileNotFoundError:
        print(f"ERRO: Arquivo de script não encontrado em '{caminho_script}'. Verifique o caminho.")
    except Exception as e:
        print(f"ERRO ao executar o script SQL: {e}")
        if db.connection:
            db.connection.rollback()
    finally:
        if db.connection:
            db.disconnect()


# --- Ponto de Entrada do Script ---
if __name__ == '__main__':
    caminho_do_script = os.path.join("sql", "main.sql")
    executar_script_sql(caminho_do_script)