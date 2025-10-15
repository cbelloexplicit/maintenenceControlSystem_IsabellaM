from src.controller.controller_usuario import ControllerUsuario
from src.model.usuario import Usuario
import hashlib

# Instancia o controlador que será usado em todos os testes
ctrl_usuario = ControllerUsuario()
novo_usuario = Usuario.__init__(id_usuario=None, nome_completo="eu",email_usuario="isa",senha_hash="lala")
ctrl_usuario.inserir_usuario(novo_usuario)
test = ctrl_usuario.listar_todos_usuarios()
print(test)