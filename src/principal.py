# IMPORTS

#BIBLIOTECAS PY
import os
import hashlib
from datetime import date, datetime

#INTERFACE E CONFIGURACAO
from src.utils.splash_screen import SplashScreen
from src.utils import ui_helper
from src.utils.config import *
from src.conexion.oracledb import OracleDB

#CLASSES MODEL
from src.model.usuario import Usuario
from src.model.empresa import Empresa
from src.model.contato import Contato
from src.model.veiculo import Veiculo
from src.model.tecnico import Tecnico
from src.model.visita_tecnica import VisitaTecnica
from src.model.lot import Lot
from src.model.catalogo_defeito import CatalogoDefeitos
from src.model.catalogo_acoes import CatalogoAcoes
from src.model.catalogo_eventos import CatalogoEventos
from src.model.defeito import Defeito
from src.model.manutencao import Manutencao
from src.model.log_lot import LogLot
from src.model.empresa_contato import EmpresaContato
from src.model.tecnico_empresa import TecnicoEmpresa

#CONTROLLERS
from src.controller.controller_usuario import ControllerUsuario
from src.controller.controller_empresa import Controller_Empresa
from src.controller.controller_contato import Controller_Contato
from src.controller.controller_tecnico import Controller_Tecnico
from src.controller.controller_veiculo import Controller_Veiculo
from src.controller.controller_lot import Controller_Lot
from src.controller.controller_visita_tecnica import Controller_VisitaTecnica
from src.controller.controller_defeito import Controller_Defeito
from src.controller.controller_manutencao import Controller_Manutencao
from src.controller.controller_loglot import Controller_LogLot
from src.controller.controller_dashboard import ControllerDashboard
from src.controller.controller_catalogo_acoes import Controller_Catalogo_Acoes
from src.controller.controller_catalogo_defeitos import Controller_Catalogo_Defeitos
from src.controller.controller_catalogo_eventos import Controller_Catalogo_Eventos

#INSTANCIA DE CONTROLLERS
ctrl_usuario = ControllerUsuario()
ctrl_empresa = Controller_Empresa()
ctrl_contato = Controller_Contato()
ctrl_tecnico = Controller_Tecnico()
ctrl_veiculo = Controller_Veiculo()
ctrl_lote = Controller_Lot()
ctrl_visita = Controller_VisitaTecnica()
ctrl_defeito = Controller_Defeito()
ctrl_manutencao = Controller_Manutencao()
ctrl_log = Controller_LogLot()
ctrl_dashboard = ControllerDashboard()
ctrl_cat_acoes = Controller_Catalogo_Acoes()
ctrl_cat_defeitos = Controller_Catalogo_Defeitos()
ctrl_cat_eventos = Controller_Catalogo_Eventos()

#FUNCOES MENU
def login():
    """
    Exibe a tela de login, valida as credenciais e gerencia as tentativas.
    Retorna o objeto do usuário logado em caso de sucesso, ou None se o usuário cancelar.
    """
    while True:
        ui_helper.limpar_tela()
        ui_helper.exibir_cabecalho("BEM VINDO! VAMOS INICIAR O SEU ACESSO:")

        # Pede as credenciais ao usuário
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        usuario_logado = ctrl_usuario.validar_login(email, senha)

        # Se o controller retornou um objeto de usuário, o login foi bem-sucedido
        if usuario_logado:
            print(f"\nLogin efetuado com sucesso! Bem-vindo(a), {usuario_logado.get_nome_completo()}.")
            input("\nPressione Enter para continuar...")
            return usuario_logado
        # Se o controller retornou None, o login falhou
        else:
            print("\nFalha na autenticação. E-mail ou senha incorretos.")
            # Usa o helper para perguntar se o usuário quer tentar novamente
            if not ui_helper.pedir_confirmacao("tentar novamente"):
                return None

def menu_principal(usuario_logado):
    print("Tudo funcionando")
#START
if __name__ == '__main__':
    #splash screen
    splash = SplashScreen()
    splash.run()
    #login - armazena usuario
    usuario = login()
    #se o login foi bem-sucedido E a tentativa de conexão com o oracle inicial deu certo, chama o menu principal
    if usuario:
        menu_principal(usuario)
    else:
        print("Encerrando o programa...")