# IMPORTS

#BIBLIOTECAS PY
import os
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

#relatorios
from src.reports.relatorios import Relatorios

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
from src.utils.ui_helper import selecionar_entidade

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
relatorios_manager = Relatorios()

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
            # Usa o helper para perguntar se o usuário quer tentar novamente
            if not ui_helper.pedir_confirmacao("tentar novamente"):
                return None

def acao_nao_implementada():
    print("Funcionalidade ainda não implementada.")
    input("\nPressione Enter para continuar...")

# MENUS DE GERENCIAMENTO DE CATÁLOGOS
def menu_gerenciar_catalogo_generico(nome_catalogo: str):
    while True:
        ui_helper.limpar_tela()
        print(f"--- Gerenciar Catálogo de {nome_catalogo} ---")
        print(MENU_CATALOGO_X)
        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            break
        elif opcao not in ['0','1','2','3','4','5']:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")
        elif nome_catalogo =="Defeitos":
            if opcao == "1":
                #inserir
            elif opcao == "2":
                #listar
            elif opcao == "3":
                #buscar
            elif opcao == "4":
                #editar
            elif opcao == "5":
                #remover
        elif nome_catalogo == "Ações":
            if opcao == "1":
                #inserir
            elif opcao == "2":
                #listar
            elif opcao == "3":
                #buscar
            elif opcao == "4":
                #editar
            elif opcao == "5":
                #remover
        elif nome_catalogo == "Eventos":
            if opcao == "1":
                #inserir
            elif opcao == "2":
                #listar
            elif opcao == "3":
                #buscar
            elif opcao == "4":
                #editar
            elif opcao == "5":
                #remover

def menu_gerenciar_catalogos(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_CATALOGOS)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciar_catalogo_generico("Defeitos")
        elif opcao == '2':
            menu_gerenciar_catalogo_generico("Ações")
        elif opcao == '3':
            menu_gerenciar_catalogo_generico("Eventos")
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENUS DE GERENCIAMENTO DE ENTIDADES
def menu_editar_empresas():
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_EMPRESAS)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2']:
            acao_nao_implementada()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


def menu_ver_detalhes_empresa():
    while True:
        ui_helper.limpar_tela()
        print(MENU_VER_DETALHES)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2', '3']:
            acao_nao_implementada()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


def menu_gerenciar_empresas():
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_EMPRESAS)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2', '4']:
            acao_nao_implementada()
        elif opcao == '3':
            menu_editar_empresas()
        elif opcao == '5':
            menu_ver_detalhes_empresa()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


def menu_editar_contatos():
    acao_nao_implementada()


def menu_gerenciar_contatos():
    acao_nao_implementada()


def menu_editar_tecnicos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_TECNICOS)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2', '3', '4', '5']:
            acao_nao_implementada()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


def menu_gerenciar_tecnicos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_TECNICOS)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2', '4']:
            acao_nao_implementada()
        elif opcao == '3':
            menu_editar_tecnicos()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

def menu_gerenciar_entidades(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_ENTIDADES)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciar_empresas()
        elif opcao == '2':
            # menu_gerenciar_contatos()
            acao_nao_implementada()
        elif opcao == '3':
            menu_gerenciar_tecnicos()
        elif opcao == '4':
            # menu_gerenciar_veiculos()
            acao_nao_implementada()
        elif opcao == '5':
            # menu_gerenciar_dispositivos()
            acao_nao_implementada()
        elif opcao == '6':
            # menu_gerenciar_usuarios()
            acao_nao_implementada()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


# ===================================================================================
# MENUS PRINCIPAIS
# ===================================================================================

def menu_registrar_operacoes(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_REGISTRAR_OPERACOES)
        opcao = input("Escolha uma opção: ")
        if opcao in ['1', '2', '3', '4']:
            acao_nao_implementada()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")


def menu_gerar_relatorios(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERAR_RELATORIOS)

        opcao = input("Escolha uma opção: ")

        #Visitas por Técnico
        if opcao == '1':
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("RELATÓRIO DE ATIVIDADES POR TÉCNICO")

            nome_busca = input("Digite o nome do técnico: ")
            tecnicos_encontrados = ctrl_tecnico.buscar_tecnicos_por_nome(nome_busca)
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_encontrados, "técnico")

            if tecnico_selecionado:
                id_tecnico = tecnico_selecionado.get_id_tecnico()
                nome_tecnico = tecnico_selecionado.get_contato().get_nome_contato()

                atividades = relatorios_manager.get_relatorio_atividades_tecnico(id_tecnico)

                ui_helper.limpar_tela()
                ui_helper.exibir_cabecalho(f"ATIVIDADES DE: {nome_tecnico.upper()}")

                if not atividades:
                    print("Nenhuma atividade encontrada para este técnico.")
                else:
                    for i, atividade in enumerate(atividades):
                        print(f"--- Atividade {i + 1} ---")
                        print(
                            f"  Data da Visita...: {atividade['data_visita'].strftime('%d/%m/%Y') if atividade['data_visita'] else 'N/A'}")
                        print(f"  Veículo..........: {atividade['veiculo_placa']}")
                        print(f"  Defeito Reportado: {atividade['defeito_reportado']}")
                        print(f"  Ação Realizada...: {atividade['acao_realizada']}")
                        print(f"  Observações......: {atividade['observacao']}\n")

            input("\nPressione Enter para voltar...")

        #manutencoes
        elif opcao == '2':
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("RELATÓRIO GERAL DE MANUTENÇÕES")
            dados_relatorio = relatorios_manager.get_relatorio_manutencoes_por_empresa()

            if not dados_relatorio:
                print("Nenhuma manutenção realizada ainda para gerar o relatório.")
            else:
                print(f"{'EMPRESA':<30} | {'TOTAL DE MANUTENÇÕES':<20}")
                print("-" * 55)

                for linha_relatorio in dados_relatorio:
                    print(f"{linha_relatorio['empresa']:<30} | {linha_relatorio['total_manutencoes']:<20}")
            input("\nPressione Enter para voltar...")

        #defeitos
        elif opcao == '3':
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("RELATÓRIO TOTAL DE DEFEITOS POR EMPRESA")

            dados_relatorio = relatorios_manager.get_relatorio_defeitos_por_empresa()

            if not dados_relatorio:
                print("Nenhum defeito encontrado para gerar o relatório.")
            else:
                print(f"{'EMPRESA':<30} | {'TOTAL DE DEFEITOS':<20}")
                print("-" * 55)
                for linha_relatorio in dados_relatorio:
                    print(f"{linha_relatorio['empresa']:<30} | {linha_relatorio['total_defeitos']:<20}")
            input("\nPressione Enter para continuar...")

        #relatorio detalhado em uma empresa x - ERRO
        '''
        elif opcao == '4':
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("RELATÓRIO DETALHADO EM UMA EMPRESA")

            nome_busca = input("Digite o nome da empresa: ")
            empresas_encontradas = ctrl_empresa.buscar_empresa_por_nome(nome_busca)
            empresa_selecionada = ui_helper.selecionar_entidade(empresas_encontradas, "empresa")

            if empresa_selecionada:
                id_empresa = empresa_selecionada.get_id_empresa()
                nome_empresa = empresa_selecionada.get_nome_fantasia()

                dados_relatorio = relatorios_manager.get_relatorio_detalhado_empresa(id_empresa)

                ui_helper.limpar_tela()
                ui_helper.exibir_cabecalho(f"RELATORIO {nome_empresa.upper()}")

                if not isinstance(dados_relatorio, dict) or not dados_relatorio:
                    print("Nenhuma informação encontrada para esta empresa.")
                else:
                    if not dados_relatorio:
                        print("Nenhuma informação encontrada nessa empresa.")
                    else:
                        for i, dados_relatorio in enumerate(dados_relatorio):
                            # Seção 1: Defeitos Atuais
                            print("\n--- DEFEITOS ATUAIS EM ABERTO ---")
                            if dados_relatorio['defeitos_atuais']:
                                for defeito in dados_relatorio['defeitos_atuais']:
                                    data_formatada = defeito['data_reporte'].strftime('%d/%m/%Y') if defeito[
                                        'data_reporte'] else 'N/A'
                                    print(
                                        f"  - Veículo: {defeito['placa']} | Reportado em: {data_formatada} | Defeito: {defeito['descricao']}")
                            else:
                                print("  Nenhum defeito em aberto para os veículos desta empresa.")

                            # Seção 2: Veículos da Frota
                            print("\n--- VEÍCULOS DA FROTA ---")
                            if dados_relatorio["veiculos"]:
                                for veiculo in dados_relatorio["veiculos"]:
                                    print(f"  - Placa: {veiculo['placa']}, Frota: {veiculo['frota']}")
                            else:
                                print("  Nenhum veículo cadastrado.")

                            # Seção 3: Técnicos Associados
                            print("\n--- TÉCNICOS ASSOCIADOS ---")
                            if dados_relatorio["tecnicos"]:
                                for tecnico in dados_relatorio["tecnicos"]:
                                    print(f"  - Nome: {tecnico['nome']}, Local: {tecnico['local']}")
                            else:
                                print("  Nenhum técnico associado.")

                            # Seção 4: Histórico de Manutenções
                            print("\n--- HISTÓRICO DE MANUTENÇÕES REALIZADAS ---")
                            if dados_relatorio["manutencoes"]:
                                for manutencao in dados_relatorio["manutencoes"]:
                                    data_formatada = manutencao['data'].strftime('%d/%m/%Y') if manutencao[
                                        'data'] else 'N/A'
                                    print(
                                        f"  - Data: {data_formatada}, Veículo: {manutencao['placa']}, Defeito: {manutencao['defeito']}, Técnico: {manutencao['tecnico']}")
                            else:
                                print("  Nenhum registro de manutenção encontrado.")
            input("\nPressione Enter para voltar...")
        '''
        #voltar
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")


def menu_principal(usuario_logado: Usuario):
    """ Exibe o menu principal e gerencia a navegação. """
    while True:
        ui_helper.limpar_tela()
        print(f"Usuário Logado: {usuario_logado.get_nome_completo()}")
        print(MENU_PRINCIPAL)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciar_entidades(usuario_logado)
        elif opcao == '2':
            menu_registrar_operacoes(usuario_logado)
        elif opcao == '3':
            menu_gerenciar_catalogos(usuario_logado)
        elif opcao == '4':
            menu_gerar_relatorios(usuario_logado)
        elif opcao == '5':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")
#START
if __name__ == '__main__':
    '''
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
    '''
    print("MODO DE TESTE: Entrando diretamente no menu principal.")
    usuario_teste = Usuario(id_usuario=99, nome_completo="Usuário de Teste", email_usuario="teste@teste.com",
                            senha="123")
    menu_principal(usuario_teste)