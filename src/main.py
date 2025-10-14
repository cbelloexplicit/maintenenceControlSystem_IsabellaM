from src.controller.controller_usuario import ControllerUsuario
from src.model.usuario import Usuario
import hashlib

# Instancia o controlador que será usado em todos os testes
ctrl_usuario = ControllerUsuario()


def run_tests():
    """
    Executa uma sequência de testes para validar todas as funcionalidades do ControllerUsuario.
    """
    print("=================================================")
    print("=      INICIANDO TESTE GERAL DO CONTROLLER      =")
    print("=================================================\n")

    # --- 1. Teste de INSERÇÃO ---
    print("\n--- [TESTE 1: INSERIR USUÁRIO] ---")
    senha_original = "senha123"
    senha_hash = hashlib.sha256(senha_original.encode()).hexdigest()
    usuario_teste = Usuario(id_usuario=None,
                            nome_completo="Usuario Teste",
                            email_usuario="teste@email.com",
                            senha_hash=senha_hash)

    if ctrl_usuario.inserir_usuario(usuario_teste):
        print("Resultado: Inserção bem-sucedida (aparente).")
    else:
        print("Resultado: FALHA na inserção.")
        return  # Para o teste se a inserção falhar

    # --- 2. Teste de LISTAR TODOS e BUSCA POR NOME ---
    print("\n--- [TESTE 2: LISTAR E BUSCAR POR NOME] ---")
    usuarios = ctrl_usuario.listar_todos_usuarios()
    if usuarios:
        print("Listando todos os usuários:")
        for user in usuarios:
            print(user.to_string())
    else:
        print("Resultado: FALHA ao listar usuários.")

    usuarios_busca = ctrl_usuario.buscar_usuario_por_nome("Teste")
    if usuarios_busca:
        print("\nBusca por nome 'Teste' encontrou:")
        for user in usuarios_busca:
            print(user.to_string())
        # Guarda o ID para os próximos testes
        id_usuario_teste = usuarios_busca[0].get_id_usuario()
    else:
        print("Resultado: FALHA na busca por nome.")
        return

    # --- 3. Teste de ATUALIZAÇÃO ---
    print("\n--- [TESTE 3: ATUALIZAR USUÁRIO] ---")
    usuario_atualizado = Usuario(id_usuario=id_usuario_teste,
                                 nome_completo="Usuario Teste Atualizado",
                                 email_usuario="teste_atualizado@email.com",
                                 senha_hash=senha_hash)  # Mantendo a mesma senha

    if ctrl_usuario.atualizar_usuario(usuario_atualizado):
        print("Resultado: Atualização bem-sucedida.")
        # Verifica a atualização
        usuarios_depois_update = ctrl_usuario.listar_todos_usuarios()
        print("\nLista de usuários após a atualização:")
        for user in usuarios_depois_update:
            print(user.to_string())
    else:
        print("Resultado: FALHA na atualização.")

    # --- 4. Teste de VALIDAÇÃO DE LOGIN ---
    print("\n--- [TESTE 4: VALIDAR LOGIN] ---")
    print("Testando com senha CORRETA...")
    usuario_logado = ctrl_usuario.validar_login(email="teste_atualizado@email.com", senha=senha_original)
    if usuario_logado:
        print(f"Resultado: Login validado com sucesso para {usuario_logado.get_nome_completo()}.")
    else:
        print("Resultado: FALHA na validação com senha correta.")

    print("\nTestando com senha INCORRETA...")
    usuario_nao_logado = ctrl_usuario.validar_login(email="teste_atualizado@email.com", senha="senha_errada")
    if not usuario_nao_logado:
        print("Resultado: Login corretamente bloqueado com senha incorreta.")
    else:
        print("Resultado: FALHA, login permitido com senha incorreta.")

    # --- 5. Teste de REMOÇÃO ---
    print("\n--- [TESTE 5: REMOVER USUÁRIO] ---")
    if ctrl_usuario.remover_usuario(id_usuario_teste):
        print(f"Resultado: Remoção do usuário ID {id_usuario_teste} bem-sucedida.")
    else:
        print("Resultado: FALHA na remoção.")

    # --- 6. Verificação Final ---
    print("\n--- [VERIFICAÇÃO FINAL] ---")
    usuarios_finais = ctrl_usuario.listar_todos_usuarios()
    print("Lista final de usuários:")
    if usuarios_finais:
        for user in usuarios_finais:
            print(user.to_string())
    else:
        print("Nenhum usuário no banco de dados.")

    # Verifica se o usuário de teste ainda existe
    ainda_existe = any(user.get_id_usuario() == id_usuario_teste for user in usuarios_finais)
    if not ainda_existe:
        print("\nVERIFICAÇÃO: Usuário de teste foi removido com sucesso do banco.")
    else:
        print("\nVERIFICAÇÃO: FALHA, usuário de teste ainda existe no banco.")

    print("\n=================================================")
    print("=              TESTE GERAL FINALIZADO           =")
    print("=================================================\n")


# --- Ponto de Entrada do Script de Teste ---
if __name__ == '__main__':
    run_tests()