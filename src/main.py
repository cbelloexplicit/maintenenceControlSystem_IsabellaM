
from src.controller.controller_dashboard import ControllerDashboard
from src.controller.controller_usuario import ControllerUsuario
from src.model.usuario import Usuario
print("Iniciando teste de inserção de usuário...")

ctrl_usuario = ControllerUsuario()
novo_usuario = Usuario(id_usuario=None,
                       nome_completo="Isabella M.",
                       email_usuario="isabella.m@teste.com",
                       senha_hash="senha_super_secreta_123")
ctrl_usuario.inserir_usuario(novo_usuario)
print("Finalizado teste de inserção de usuário.\n")
print("Iniciando teste do dashboard...")
dashboard_controller = ControllerDashboard()
contagens = dashboard_controller.obter_contagem_registros()

print("\nContagem de registros no banco:")
print(contagens)
print("Finalizado teste do dashboard.")