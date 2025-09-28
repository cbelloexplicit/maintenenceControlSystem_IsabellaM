# Em principal.py (exemplo de teste)
from model.tecnico import Tecnico
from controller.controller_tecnico import Controller_Tecnico

# Cria um objeto Tecnico
novo_tecnico = Tecnico(id_tecnico=None, nome_tecnico="Joao da Silva") # O ID pode ser None, pois o Oracle vai gerar

# Cria uma instância do controlador e chama o método de inserção
ctrl_tecnico = Controller_Tecnico()
ctrl_tecnico.inserir_tecnico(novo_tecnico)