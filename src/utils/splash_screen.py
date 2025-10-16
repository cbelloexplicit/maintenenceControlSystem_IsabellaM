# Arquivo: src/utils/splash_screen.py

from src.controller.controller_dashboard import ControllerDashboard
from src.utils import ui_helper


class SplashScreen:

    def __init__(self):
        self.ctrl_dashboard = ControllerDashboard()

    def run(self):
        ui_helper.limpar_tela()
        contagens = self.ctrl_dashboard.obter_contagem_registros()

        print("################################################")
        print("#       SISTEMA DE CONTROLE DE MANUTENÇÃO      #")
        print("################################################")

        print("\nResumo de Registros no Banco de Dados:")

        if contagens:
            for tabela, total in contagens.items():
                print(f"- {tabela.capitalize():<15}: {total} registros")
        else:
            print("Não foi possível carregar o resumo de registros.")

        print("\nCriado por:")
        print("- Isabella M.")

        print("\nDisciplina: Banco de Dados")
        print("Professor: Howard Roatti")
        print("################################################\n")

        input("Pressione Enter para continuar...")