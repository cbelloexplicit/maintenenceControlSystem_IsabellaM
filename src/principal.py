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

# FUNCOES DE GERENCIAMENTO DE CATALOGOS
def inserir_novo_defeito_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("INSERIR NOVO DEFEITO NO CATÁLOGO")
    
    codigo = input("Digite o código para o novo defeito (ex: FALHA_SENSOR): ").strip().upper()
    descricao = input("Digite a descrição do defeito: ").strip()

    if not codigo:
        print("Erro: O código do defeito é obrigatório.")
        input("\nPressione Enter para continuar...")
        return

    novo_defeito_cat_obj = CatalogoDefeitos(id_catalogo_defeito=None, codigo_defeito=codigo, descricao_defeito=descricao)

    if ui_helper.pedir_confirmacao(f"inserir o defeito '{codigo}' no catálogo"):
        if ctrl_cat_defeitos.inserir_defeito(novo_defeito_cat_obj):
            print("\nDefeito inserido no catálogo com sucesso!")
        
    input("\nPressione Enter para continuar...")

def inserir_nova_acao_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("INSERIR NOVA AÇÃO NO CATÁLOGO")

    codigo = input("Digite o código para a nova ação (ex: MANUTENCAO_SIMPLES): ").strip().upper()
    descricao = input("Digite a descrição da ação: ").strip()

    if not codigo:
        print("Erro: O código da ação é obrigatória.")
        input("\nPressione Enter para continuar...")
        return

    nova_acao_cat_obj = CatalogoAcoes(id_catalogo_acao=None, codigo_acao=codigo, descricao_acao=descricao)

    if ui_helper.pedir_confirmacao(f"inserir a ação '{codigo}' no catálogo"):
        if ctrl_cat_acoes.inserir_acao(nova_acao_cat_obj):
            print("\nAção inserida no catálogo com sucesso!")
        
    input("\nPressione Enter para continuar...")

def inserir_novo_evento_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("INSERIR NOVO EVENTO NO CATÁLOGO")

    codigo = input("Digite o código para o novo evento (ex: INSTALACAO): ").strip().upper()

    if not codigo:
        print("Erro: O código do evento é obrigatório.")
        input("\nPressione Enter para continuar...")
        return

    novo_evento_cat_obj = CatalogoEventos(id_catalogo_eventos=None, codigo_evento=codigo)

    if ui_helper.pedir_confirmacao(f"inserir o evento '{codigo}' no catálogo"):
        if ctrl_cat_eventos.inserir_evento(novo_evento_cat_obj):
            print("\nEvento inserida no catálogo com sucesso!")
        
    input("\nPressione Enter para continuar...")

def listar_todos_defeitos_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("CATÁLOGO DE DEFEITOS")
    
    lista_defeitos = ctrl_cat_defeitos.listar_defeitos()
    
    if not lista_defeitos:
        print("Nenhum defeito cadastrado no catálogo.")
    else:
        print(f"{'ID':<5} | {'CÓDIGO':<25} | {'DESCRIÇÃO':<40}")
        print("-" * 75)
        for defeito in lista_defeitos:
            print(f"{defeito.get_id_catalogo_defeito():<5} | {defeito.get_codigo_defeito():<25} | {defeito.get_descricao_defeito():<40}")
            
    input("\nPressione Enter para continuar...")

def listar_todas_acoes_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("CATÁLOGO DE AÇÕES")
    
    lista_acoes = ctrl_cat_acoes.listar_acoes()
    
    if not lista_acoes:
        print("Nenhuma ação cadastrada no catálogo.")
    else:
        print(f"{'ID':<5} | {'CÓDIGO':<25} | {'DESCRIÇÃO':<40}")
        print("-" * 75)
        for acao in lista_acoes:
            print(f"{acao.get_id_catalogo_acao():<5} | {acao.get_codigo_acao():<25} | {acao.get_descricao_acao():<40}")
            
    input("\nPressione Enter para continuar...")

def listar_todos_eventos_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("CATÁLOGO DE EVENTOS")
    
    lista_eventos = ctrl_cat_eventos.listar_eventos()
    
    if not lista_eventos:
        print("Nenhum defeito cadastrado no catálogo.")
    else:
        print(f"{'ID':<5} | {'CÓDIGO':<25}")
        print("-" * 75)
        for evento in lista_eventos:
            print(f"{evento.get_id_catalogo_eventos():<5} | {evento.get_codigo_evento():<25}")
            
    input("\nPressione Enter para continuar...")

def buscar_defeito_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("BUSCAR DEFEITO NO CATÁLOGO")
    codigo_busca = input("Digite o código do defeito a ser buscado: ").strip().upper()
    
    defeito_encontrado = ctrl_cat_defeitos.buscar_defeito_por_codigo(codigo_busca)
    
    if defeito_encontrado:
        print("\nDefeito encontrado:")
        print(defeito_encontrado.to_string())
    else:
        print(f"\nNenhum defeito encontrado com o código '{codigo_busca}'.")
        
    input("\nPressione Enter para continuar...")

def buscar_acao_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("BUSCAR AÇÃO NO CATÁLOGO")
    
    codigo_busca = input("Digite o código da ação a ser buscada: ").strip().upper()
    
    acao_encontrada = ctrl_cat_acoes.buscar_acao_por_codigo(codigo_busca)
    
    if acao_encontrada:
        print("\nAção encontrada:")
        print(acao_encontrada.to_string())
    else:
        print(f"\nNenhuma ação encontrada com o código '{codigo_busca}'.")

    input("\nPressione Enter para continuar...")

def buscar_evento_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("BUSCAR EVENTO NO CATÁLOGO")
    
    codigo_busca = input("Digite o código do evento a ser buscado: ").strip().upper()
    evento_encontrado = ctrl_cat_eventos.buscar_evento_por_codigo(codigo_busca)
    
    if evento_encontrado:
        print("\nEvento encontrado:")
        print(evento_encontrado.to_string())
    else:
        print(f"\nNenhum evento encontrado com o código '{codigo_busca}'.")
        
    input("\nPressione Enter para continuar...")

def editar_defeito_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("EDITAR DEFEITO DO CATÁLOGO")
    
    print("Selecione o defeito que deseja editar:")
    lista_defeitos = ctrl_cat_defeitos.listar_defeitos()
    defeito_selecionado = ui_helper.selecionar_entidade(lista_defeitos, "defeito do catálogo")

    if defeito_selecionado:
        print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
        novo_codigo = input(f"Novo código ({defeito_selecionado.get_codigo_defeito()}): ").strip().upper()
        nova_descricao = input(f"Nova descrição ({defeito_selecionado.get_descricao_defeito()}): ").strip()

        if novo_codigo:
            defeito_selecionado.set_codigo_defeito(novo_codigo)
        if nova_descricao:
            defeito_selecionado.set_descricao_defeito(nova_descricao)

        if ui_helper.pedir_confirmacao("atualizar este defeito do catálogo"):
            ctrl_cat_defeitos.atualizar_defeito(defeito_selecionado)

    input("\nPressione Enter para continuar...")

def editar_evento_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("EDITAR EVENTO DO CATÁLOGO")
    
    print("Selecione o evento que deseja editar:")
    lista_eventos = ctrl_cat_eventos.listar_eventos()
    evento_selecionado = ui_helper.selecionar_entidade(lista_eventos, "evento do catálogo")

    if evento_selecionado:
        print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
        novo_codigo = input(f"Novo código ({evento_selecionado.get_codigo_evento()}): ").strip().upper()

        if novo_codigo:
            evento_selecionado.set_codigo_evento(novo_codigo)
        if ui_helper.pedir_confirmacao("atualizar este defeito do catálogo"):
            ctrl_cat_eventos.atualizar_evento(evento_selecionado)

    input("\nPressione Enter para continuar...")

def editar_acao_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("EDITAR AÇÃO DO CATÁLOGO")
    
    print("Selecione a ação que deseja editar:")
    lista_acao = ctrl_cat_acoes.listar_acoes()
    acao_selecionada = ui_helper.selecionar_entidade(lista_acao, "ação do catálogo")

    if acao_selecionada:
        print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
        novo_codigo = input(f"Novo código ({acao_selecionada.get_codigo_acao()}): ").strip().upper()
        nova_descricao = input(f"Nova descrição ({acao_selecionada.get_descricao_acao()}): ").strip()

        if novo_codigo:
            acao_selecionada.set_codigo_acao(novo_codigo)
        if nova_descricao:
            acao_selecionada.set_descricao_acao(nova_descricao)

        if ui_helper.pedir_confirmacao("atualizar este defeito do catálogo"):
            ctrl_cat_acoes.atualizar_acao(acao_selecionada)

    input("\nPressione Enter para continuar...")

def remover_defeito_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("REMOVER DEFEITO DO CATÁLOGO")

    print("Selecione o defeito que deseja remover:")
    lista_defeitos = ctrl_cat_defeitos.listar_defeitos()
    defeito_selecionado = ui_helper.selecionar_entidade(lista_defeitos, "defeito do catálogo")

    if defeito_selecionado:
        acao = f"remover o defeito '{defeito_selecionado.get_codigo_defeito()}' do catálogo"
        if ui_helper.pedir_confirmacao(acao):
            ctrl_cat_defeitos.remover_defeito(defeito_selecionado.get_id_catalogo_defeito())
            
    input("\nPressione Enter para continuar...")

def remover_acao_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("REMOVER AÇÃO DO CATÁLOGO")

    print("Selecione a ação que deseja remover:")
    lista_acoes = ctrl_cat_acoes.listar_acoes()
    acao_selecionada = ui_helper.selecionar_entidade(lista_acoes, "ação do catálogo")

    if acao_selecionada:
        acao = f"remover a ação '{acao_selecionada.get_codigo_acao()}' do catálogo"
        if ui_helper.pedir_confirmacao(acao):
            ctrl_cat_acoes.remover_acao(acao_selecionada.get_id_catalogo_acao())
            
    input("\nPressione Enter para continuar...")

def remover_evento_catalogo():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("REMOVER EVENTO DO CATÁLOGO")

    print("Selecione o evento que deseja remover:")
    lista_evento = ctrl_cat_eventos.listar_eventos()
    evento_selecionado = ui_helper.selecionar_entidade(lista_evento, "evento do catálogo")

    if evento_selecionado:
        acao = f"remover o evento '{evento_selecionado.get_codigo_evento()}' do catálogo"
        if ui_helper.pedir_confirmacao(acao):
            ctrl_cat_eventos.remover_evento(evento_selecionado.get_id_catalogo_eventos())
            
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
                inserir_novo_defeito_catalogo()
            elif opcao == "2":
                listar_todos_defeitos_catalogo()
            elif opcao == "3":
                buscar_defeito_catalogo()
            elif opcao == "4":
                editar_defeito_catalogo()
            elif opcao == "5":
                remover_defeito_catalogo()
        elif nome_catalogo == "Ações":
            if opcao == "1":
                inserir_nova_acao_catalogo()
            elif opcao == "2":
                listar_todas_acoes_catalogo()
            elif opcao == "3":
                buscar_acao_catalogo()
            elif opcao == "4":
                editar_acao_catalogo()
            elif opcao == "5":
                remover_acao_catalogo()
        elif nome_catalogo == "Eventos":
            if opcao == "1":
                inserir_novo_evento_catalogo()
            elif opcao == "2":
                listar_todos_eventos_catalogo()
            elif opcao == "3":
                buscar_evento_catalogo()
            elif opcao == "4":
                editar_evento_catalogo()
            elif opcao == "5":
                remover_evento_catalogo()

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

# FUNÇÕES DE GERENCIAMENTO DE ENTIDADES
# MENUS DE GERENCIAMENTO DE EMPRESAS
def menu_editar_empresas():
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_EMPRESAS)
        opcao = input("Escolha uma opção: ")

        escolha = input("Pesquise a empresa que deseja editar: ")
        lista_opcoes = ctrl_empresa.buscar_empresa_por_nome(escolha)
        empresa_selecionada = ui_helper.selecionar_entidade(lista_opcoes, 'empresa')

        if opcao == "1":
        #atualizar
            ui_helper.exibir_cabecalho("ATUALIZAR EMPRESA NO CATÁLOGO")    
            if empresa_selecionada:
                print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
                novo_nome = input(f"Novo nome fantasia ({empresa_selecionada.get_nome_fantasia()}): ").strip().upper()
                novo_endereco = input(f"Nova descrição ({empresa_selecionada.get_endereco()}): ").strip()

            if novo_nome:
                empresa_selecionada.set_nome_fantasia(novo_nome)
            if novo_endereco:
                empresa_selecionada.set_endereco(novo_endereco)
            if ui_helper.pedir_confirmacao("atualizar esta empresa do catálogo"):
                ctrl_empresa.atualizar_empresa(empresa_selecionada)

            input("\nPressione Enter para continuar...")
        
        elif opcao == '2':
        #remover
            ui_helper.exibir_cabecalho("REMOVER EMPRESA DO CATÁLOGO")

            if empresa_selecionada:
                acao = f"remover a empresa '{empresa_selecionada.get_nome_fantasia()}' do catálogo"
                if ui_helper.pedir_confirmacao(acao):
                    ctrl_empresa.remover_empresa(empresa_selecionada.get_id_empresa())
                    
            input("\nPressione Enter para continuar...")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

def menu_ver_detalhes_empresa():
    while True:
        ui_helper.limpar_tela()
        #escolher empresa antes
        ui_helper.limpar_tela()
        print(MENU_EDITAR_EMPRESAS)
        opcao = input("Escolha uma opção: ")

        escolha = input("Pesquise a empresa que deseja editar: ")
        lista_opcoes = ctrl_empresa.buscar_empresa_por_nome(escolha)
        empresa_selecionada = ui_helper.selecionar_entidade(lista_opcoes, 'empresa')

        print(MENU_VER_DETALHES)
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
        #lista veículo
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho(f"LISTA DE VEÍCULOS EM {empresa_selecionada}")
            
            lista_veículos = ctrl_empresa.listar_veiculos_em_empresa(empresa_selecionada)
            if not lista_veículos:
                print("A empresa não possui veículos atribuidos a ela.")
            else:
                print(f"{'ID':<5} | {'PLACA':<10} | {'FROTA':<10}")
                print("-" * 75)
                for veiculo in lista_veículos:
                    print(f"{veiculo.get_id_veiculo():<5} | {veiculo.get_placa():<10} | {veiculo.get_frota():<10}")
                    
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
        #lista contato
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho(f"LISTA DE CONTATOS EM {empresa_selecionada}")
            
            lista_contatos = ctrl_empresa.listar_contatos_da_empresa(empresa_selecionada)
            if not lista_contatos:
                print("A empresa não possui contatos atribuidos a ela.")
            else:
                print(f"{'ID':<5} | {'NOME':<25} | {'EMAIL':<30} | {'TELEFONE':<15}")
                print("-" * 75)
                for contato in lista_contatos:
                    print(f"{contato.get_id_contato():<5} | {contato.get_nome_contato():<10} | {contato.get_email_contato():<10} | {contato.get_telefone():<15}")
                    
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
        #lista tecnicos
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho(f"LISTA DE TÉCNICOS EM {empresa_selecionada}")
            
            lista_tecnicos = ctrl_empresa.listar_tecnicos_em_empresa(empresa_selecionada)
            if not lista_tecnicos:
                print("A empresa não possui tecnicos atribuidos a ela.")
            else:
                print(f"{'ID':<5} | {'NOME':<25} | {'EMAIL':<30} | {'TELEFONE':<15}")
                print("-" * 75)
                for linha in lista_tecnicos:
                    print(f"{linha.get_id_tecnico():<5} | {linha.get_nome_contato():<10} | {contato.get_telefone():<15}")
                    
            input("\nPressione Enter para continuar...")
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
        if opcao == '1':
            #cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("INSERIR NOVA EMPRESA NO CATÁLOGO")
            
            nome = input("Digite o nome da nova empresa: ").strip().upper()
            endereco = input("Digite o endereço da empresa: ").strip()

            if not nome:
                print("Erro: O nome da empresa é obrigatória.")
                input("\nPressione Enter para continuar...")
                return
            
            if not endereco:
                print("Erro: O endereço é obrigatório.")
                input("\nPressione Enter para continuar...")
                return

            nova_empresa = Empresa(id_empresa=None, nome_fantasia=nome, endereco=endereco)

            if ui_helper.pedir_confirmacao(f"inserir a empresa '{nome}' no catálogo"):
                if ctrl_empresa.inserir_empresa(nova_empresa):
                    print("\nEmpresa inserida no catálogo com sucesso!")
                
            input("\nPressione Enter para continuar...")

        elif opcao == "2":
            #buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR EMPRESA NO CATÁLOGO")
            busca = input("Digite a empresa a procurar: ")
            if not busca:
                print("Busca inválida.")
            else:
                lista_resultado = ctrl_empresa.buscar_empresa_por_nome(busca)
                print("Resultado da busca: ")
                print("***")
                for resultado in lista_resultado:
                    print(resultado.to_string())
                    print("***")
            
        elif opcao == '3':
            #editar
            menu_editar_empresas()
        elif opcao == "4":
            #listar empresas
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE EMPRESAS")

            lista_empresas = ctrl_empresa.listar_empresas()
            for empresa in lista_empresas:
                print(f"{empresa.get_id_empresa()} | {empresa.get_nome_fantasia()} | {empresa.get_endereco()}")

        elif opcao == '5':
            #ver detalhes
            menu_ver_detalhes_empresa()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENU DE GERENCIAMENTO DE CONTATOS
def menu_editar_contatos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_CONTATOS)
        opcao = input("Escolha uma opção: ")

        escolha = input("Pesquise o contato que deseja editar: ")
        lista_opcoes = ctrl_contato.buscar_contato_por_nome(escolha)
        contato_selecionado = ui_helper.selecionar_entidade(lista_opcoes, 'contato')

        if opcao == '1':
            #1 atualizar
            ui_helper.exibir_cabecalho("ATUALIZAR CONTATO NO CATÁLOGO")    
            if contato_selecionado:
                print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
                novo_nome = input(f"Novo nome ({contato_selecionado.get_nome_contato()}): ").strip().upper()
                novo_email = input(f"Novo email ({contato_selecionado.get_email_contato()}): ").strip()
                novo_telefone = input(f"Novo telefone de contato ({contato_selecionado.get_telefone()})").strip()

            if novo_nome:
                contato_selecionado.set_nome_contato(novo_nome)
            if novo_email:
                contato_selecionado.set_email_contato(novo_email)
            if novo_telefone:
                contato_selecionado.set_telefone(novo_telefone)
            if ui_helper.pedir_confirmacao("atualizar este contato do catálogo"):
                ctrl_contato.atualizar_contato(contato_selecionado)

            input("\nPressione Enter para continuar...")

        elif opcao == '2':
            #2 remover
            ui_helper.exibir_cabecalho("REMOVER CONTATO")

            if contato_selecionado:
                acao = f"remover o contato '{contato_selecionado.get_nome_contato()}'"
                if ui_helper.pedir_confirmacao(acao):
                    ctrl_contato.remover_contato(contato_selecionado.get_id_contato())
                    
            input("\nPressione Enter para continuar...")        
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

def menu_gerenciar_contatos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_CONTATOS)
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
        #1 cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("CADASTRAR NOVO CONTATO")
            
            nome = input("Digite o nome do novo contato: ").strip()
            email = input("Digite o e-mail do contato (opcional, deixe em branco se não tiver): ").strip()
            telefone = input("Digite o telefone do contato (opcional, deixe em branco se não tiver): ").strip()

            if not nome:
                print("\nErro: O nome do contato é obrigatório.")
                input("\nPressione Enter para continuar...")
                return
                
            if not email and not telefone:
                print("\nErro: É necessário informar ao menos um e-mail OU um telefone.")
                input("\nPressione Enter para continuar...")
                return

            novo_contato_obj = Contato(id_contato=None, 
                                    nome_contato=nome, 
                                    email_contato=email if email else None, 
                                    telefone=telefone if telefone else None)

            if ui_helper.pedir_confirmacao(f"cadastrar o contato '{nome}'"):
                if ctrl_contato.inserir_contato(novo_contato_obj):
                    print("\nContato cadastrado com sucesso!")
                else:
                    print("\nFalha ao cadastrar contato.") 
                    
            input("\nPressione Enter para continuar...")

        elif opcao == '2':
        #2 buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR CONTATO")
            nome_busca = input("Digite o nome ou parte do nome do contato a procurar: ")
            
            if not nome_busca.strip():
                print("Busca inválida. Por favor, digite um nome.")
            else:
                lista_resultado = ctrl_contato.buscar_contato_por_nome(nome_busca)
                
                if not lista_resultado:
                    print(f"\nNenhum contato encontrado com o nome '{nome_busca}'.")
                else:
                    print("\nResultado da busca:")
                    for contato in lista_resultado:
                        print(contato.to_string())
                        
            input("\nPressione Enter para continuar...")
        elif opcao == '3':
        #3editar
            menu_editar_contatos()
        elif opcao == '4':
        #4listar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE CONTATOS")

            lista_contatos = ctrl_contato.listar_contatos()
            
            if not lista_contatos:
                print("Nenhum contato cadastrado.")
            else:
                print(f"{'ID':<5} | {'NOME':<30} | {'E-MAIL':<30} | {'TELEFONE':<15}")
                print("-" * 85)
                for contato in lista_contatos:
                    print(f"{contato.get_id_contato():<5} | {contato.get_nome_contato():<30} | {(contato.get_email_contato() or ''):<30} | {(contato.get_telefone() or ''):<15}")

            input("\nPressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENU DE GERENCIAMENTO DE TECNICOS
def menu_editar_tecnicos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_TECNICOS)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            #inativar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("INATIVAR TÉCNICO")
            
            print("Selecione o técnico que deseja inativar:")
            tecnicos_ativos = ctrl_tecnico.listar_tecnicos(apenas_ativos=True)
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_ativos, "técnico ativo")

            if tecnico_selecionado:
                nome_tecnico = tecnico_selecionado.get_contato().get_nome_contato() if tecnico_selecionado.get_contato() else "N/A"
                if ui_helper.pedir_confirmacao(f"inativar o técnico '{nome_tecnico}'"):
                    ctrl_tecnico.inativar_tecnico(tecnico_selecionado.get_id_tecnico())
                    
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #ativar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REATIVAR TÉCNICO")
            
            print("Selecione o técnico que deseja reativar:")
            tecnicos_todos = ctrl_tecnico.listar_tecnicos(apenas_ativos=False)
            tecnicos_inativos = [t for t in tecnicos_todos if t.get_status() == 'INATIVO'] 

            if not tecnicos_inativos:
                print("\nNenhum técnico inativo encontrado.")
                input("\nPressione Enter para continuar...")
                return

            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_inativos, "técnico inativo")

            if tecnico_selecionado:
                nome_tecnico = tecnico_selecionado.get_contato().get_nome_contato() if tecnico_selecionado.get_contato() else "N/A"
                if ui_helper.pedir_confirmacao(f"reativar o técnico '{nome_tecnico}'"):
                    ctrl_tecnico.ativar_tecnico(tecnico_selecionado.get_id_tecnico())
                    
            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            #associar a empresa
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("ASSOCIAR TÉCNICO A EMPRESA")

            print("Selecione o técnico:")
            # Lista todos os técnicos, ativos ou inativos, para associação
            tecnicos = ctrl_tecnico.listar_tecnicos(apenas_ativos=False) 
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos, "técnico")
            if not tecnico_selecionado:
                input("\nPressione Enter para continuar...")
                return

            print("\nSelecione a empresa:")
            empresas = ctrl_empresa.listar_empresas()
            empresa_selecionada = ui_helper.selecionar_entidade(empresas, "empresa")
            if not empresa_selecionada:
                input("\nPressione Enter para continuar...")
                return

            nome_tecnico = tecnico_selecionado.get_contato().get_nome_contato() if tecnico_selecionado.get_contato() else "N/A"
            if ui_helper.pedir_confirmacao(f"associar '{nome_tecnico}' à empresa '{empresa_selecionada.get_nome_fantasia()}'"):
                ctrl_tecnico.associar_tecnico_empresa(tecnico_selecionado.get_id_tecnico(), empresa_selecionada.get_id_empresa())
                
            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            #desassociar a empresa
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("DESASSOCIAR TÉCNICO DE EMPRESA")

            print("Selecione o técnico:")
            tecnicos = ctrl_tecnico.listar_tecnicos(apenas_ativos=False)
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos, "técnico")
            if not tecnico_selecionado:
                input("\nPressione Enter para continuar...")
                return
        elif opcao == '5':
            #atualizar  
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("ATUALIZAR DADOS DO TÉCNICO")
            
            print("Selecione o técnico que deseja atualizar:")
            tecnicos_todos = ctrl_tecnico.listar_tecnicos(apenas_ativos=False)
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_todos, "técnico")

            if tecnico_selecionado:
                print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
                
                novo_local = input(f"Novo local ({tecnico_selecionado.get_local()}): ").strip()
                
                print("\nPara alterar o contato associado, utilize a opção de cadastro de contatos.")
                
                objeto_atualizado = False
                if novo_local:
                    tecnico_selecionado.set_local(novo_local)
                    objeto_atualizado = True

                if objeto_atualizado:
                    if ui_helper.pedir_confirmacao("atualizar os dados deste técnico"):
                        ctrl_tecnico.atualizar_tecnico(tecnico_selecionado)
                else:
                    print("\nNenhum dado alterado.")

            input("\nPressione Enter para continuar...")
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
        if opcao == '1':
            #cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("CADASTRAR NOVO TÉCNICO")
            contato_associado = None

            while True:
                print("O técnico precisa estar associado a um registro de Contato.")
                print("1 - Usar um Contato existente")
                print("2 - Cadastrar um Novo Contato")
                print("0 - Cancelar")
                opcao_contato = input("Escolha uma opção: ")

                if opcao_contato == '1':
                    nome_contato = input("\nDigite o nome do contato existente: ")
                    contatos_encontrados = ctrl_contato.buscar_contato_por_nome(nome_contato)
                    contato_selecionado = ui_helper.selecionar_entidade(contatos_encontrados, "contato")
                    if contato_selecionado:
                        contato_associado = contato_selecionado
                        break 
                    else:
                        if not ui_helper.pedir_confirmacao("tentar buscar outro contato"):
                            print("Cadastro de técnico cancelado.")
                            input("\nPressione Enter para continuar...")
                            return 
                
                elif opcao_contato == '2':
                    ui_helper.limpar_tela()
                    ui_helper.exibir_cabecalho("CADASTRAR NOVO CONTATO")
                    
                    nome = input("Digite o nome do novo contato: ").strip()
                    email = input("Digite o e-mail do contato (opcional, deixe em branco se não tiver): ").strip()
                    telefone = input("Digite o telefone do contato (opcional, deixe em branco se não tiver): ").strip()

                    if not nome:
                        print("\nErro: O nome do contato é obrigatório.")
                        input("\nPressione Enter para continuar...")
                        return
                        
                    if not email and not telefone:
                        print("\nErro: É necessário informar ao menos um e-mail OU um telefone.")
                        input("\nPressione Enter para continuar...")
                        return

                    novo_contato_obj = Contato(id_contato=None, 
                                            nome_contato=nome, 
                                            email_contato=email if email else None, 
                                            telefone=telefone if telefone else None)

                    if ui_helper.pedir_confirmacao(f"cadastrar o contato '{nome}'"):
                        if ctrl_contato.inserir_contato(novo_contato_obj):
                            print("\nContato cadastrado com sucesso!")
                            contato_associado = novo_contato_obj
                        else:
                            print("\nFalha ao cadastrar contato.") 
                    input("\nPressione Enter para continuar...")
                    
                        
                elif opcao_contato == '0':
                    print("Cadastro de técnico cancelado.")
                    input("\nPressione Enter para continuar...")
                    return 
                
                else:
                    print("Opção inválida!")
                    input("\nPressione Enter para continuar...")
                    ui_helper.limpar_tela() 

            print(f"\nContato selecionado: {contato_associado.to_string()}")
            
            local = input("Digite o local de atuação do técnico: ").strip()
            if not local:
                print("Erro: O local de atuação é obrigatório.")
                input("\nPressione Enter para continuar...")
                return

            novo_tecnico_obj = Tecnico(id_tecnico=None, local=local, contato=contato_associado, status='ATIVO') 
            
            if ui_helper.pedir_confirmacao(f"cadastrar '{contato_associado.get_nome_contato()}' como técnico"):
                if ctrl_tecnico.inserir_tecnico(novo_tecnico_obj):
                    print("\nTécnico cadastrado com sucesso!")
                else:
                    print("\nFalha ao cadastrar técnico.")
                    
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR TÉCNICO")
            nome_busca = input("Digite o nome ou parte do nome do técnico a procurar: ")
            
            if not nome_busca.strip():
                print("Busca inválida. Por favor, digite um nome.")
            else:
                lista_resultado = ctrl_tecnico.buscar_tecnicos_por_nome(nome_busca)
                
                if not lista_resultado:
                    print(f"\nNenhum técnico (ativo) encontrado com o nome '{nome_busca}'.")
                else:
                    print("\nTécnicos ativos encontrados:")
                    for tecnico in lista_resultado:
                        print(tecnico.to_string())
                        
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
            #editar
            menu_editar_tecnicos()
        elif opcao == '4':
            #listar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE TÉCNICOS ATIVOS")

            lista_tecnicos = ctrl_tecnico.listar_tecnicos(apenas_ativos=True)
            
            if not lista_tecnicos:
                print("Nenhum técnico ativo cadastrado.")
            else:
                print(f"{'ID':<5} | {'NOME':<30} | {'LOCAL':<20} | {'STATUS':<8}")
                print("-" * 70)
                for tecnico in lista_tecnicos:
                    nome_contato = tecnico.get_contato().get_nome_contato() if tecnico.get_contato() else "N/A"
                    print(f"{tecnico.get_id_tecnico():<5} | {nome_contato:<30} | {tecnico.get_local():<20} | {tecnico.get_status():<8}")

            input("\nPressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

#FUNCAO PARA BUSCAR MANUTENCAO EM VEICULO
def buscar_manutencao_interface():
    ui_helper.limpar_tela()
    ui_helper.exibir_cabecalho("BUSCAR MANUTENÇÕES POR VEÍCULO")

    placa_busca = input("Digite a placa do veículo para ver o histórico de manutenções: ").strip().upper()

    if not placa_busca:
        print("Busca inválida. Por favor, digite uma placa.")
        input("\nPressione Enter para continuar...")
        return

    veiculo_encontrado = ctrl_veiculo.buscar_veiculo_por_placa(placa_busca)

    if not veiculo_encontrado:
        print(f"\nNenhum veículo encontrado com a placa '{placa_busca}'.")
        input("\nPressione Enter para continuar...")
        return

    id_veiculo = veiculo_encontrado.get_id_veiculo()
    print(f"\nBuscando manutenções para o veículo: {veiculo_encontrado.to_string()}")
    
    lista_manutencoes = ctrl_manutencao.listar_manutencao_em_veiculo(id_veiculo)

    if not lista_manutencoes:
        print("\nNenhuma manutenção encontrada para este veículo.")
    else:
        print("\n--- Histórico de Manutenções ---")
        print(f"  {'ID':<5} | {'DATA VISITA':<12} | {'TÉCNICO':<25} | {'AÇÃO':<30} | {'DEFEITO':<30}")
        print("  " + "-" * 110)
        for manutencao in lista_manutencoes:
            visita = manutencao.get_visita()
            acao = manutencao.get_catalogo_acao()
            defeito = manutencao.get_defeito()
            tecnico = visita.get_tecnico() if visita else None
            contato_tecnico = tecnico.get_contato() if tecnico else None
            cat_defeito = defeito.get_catalogo_defeito() if defeito else None

            data_f = visita.get_data_visita().strftime('%d/%m/%Y') if visita else 'N/A'
            nome_tecnico = contato_tecnico.get_nome_contato() if contato_tecnico else 'N/A'
            desc_acao = acao.get_descricao_acao() if acao else 'N/A'
            desc_defeito = cat_defeito.get_descricao_defeito() if cat_defeito else 'N/A'
            
            desc_acao = (desc_acao[:27] + '...') if len(desc_acao) > 30 else desc_acao
            desc_defeito = (desc_defeito[:27] + '...') if len(desc_defeito) > 30 else desc_defeito

            print(f"  {manutencao.get_id_manutencao():<5} | {data_f:<12} | {nome_tecnico:<25} | {desc_acao:<30} | {desc_defeito:<30}")

    input("\nPressione Enter para continuar...")
# MENU DE GERENCIAMENTO DE VEÍCULOS
def menu_gerenciar_veiculos():
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_VEICULOS) 
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            #cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("CADASTRAR NOVO VEÍCULO")

            print("Selecione a empresa proprietária do veículo:")
            empresas = ctrl_empresa.listar_empresas()
            empresa_selecionada = ui_helper.selecionar_entidade(empresas, "empresa")
            if not empresa_selecionada:
                input("\nPressione Enter para continuar...")
                return

            placa = input("Digite a placa do veículo (Ex: ABC1D23): ").strip().upper()
            frota = input("Digite o código da frota (opcional): ").strip()

            if not placa:
                print("\nErro: A placa é obrigatória.")
                input("\nPressione Enter para continuar...")
                return
            if len(placa) != 7: 
                print("\nErro: Formato da placa inválido (deve ter 7 caracteres).")
                input("\nPressione Enter para continuar...")
                return

            novo_veiculo_obj = Veiculo(id_veiculo=None,
                                    placa=placa,
                                    frota=frota if frota else None,
                                    empresa=empresa_selecionada)

            if ui_helper.pedir_confirmacao(f"cadastrar o veículo com placa '{placa}'"):
                if ctrl_veiculo.inserir_veiculo(novo_veiculo_obj):
                    print("\nVeículo cadastrado com sucesso!")
                else:
                    print("\nFalha ao cadastrar veículo.") 

            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #listar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE VEÍCULOS")

            lista_veiculos = ctrl_veiculo.listar_veiculos()

            if not lista_veiculos:
                print("Nenhum veículo cadastrado.")
            else:
                print(f"{'ID':<5} | {'PLACA':<10} | {'FROTA':<15} | {'EMPRESA':<30}")
                print("-" * 70)
                for veiculo in lista_veiculos:
                    nome_empresa = veiculo.get_empresa().get_nome_fantasia() if veiculo.get_empresa() else "N/A"
                    print(f"{veiculo.get_id_veiculo():<5} | {veiculo.get_placa():<10} | {(veiculo.get_frota() or ''):<15} | {nome_empresa:<30}")

            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            #buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR VEÍCULO POR PLACA")
            placa_busca = input("Digite a placa do veículo a procurar: ").strip().upper()

            if not placa_busca:
                print("Busca inválida. Por favor, digite uma placa.")
            else:
                veiculo_encontrado = ctrl_veiculo.buscar_veiculo_por_placa(placa_busca)

                if not veiculo_encontrado:
                    print(f"\nNenhum veículo encontrado com a placa '{placa_busca}'.")
                else:
                    print("\nVeículo encontrado:")
                    print(veiculo_encontrado.to_string())
                    lote_instalado = ctrl_veiculo.buscar_lote_instalado(veiculo_encontrado.get_id_veiculo())
                    if lote_instalado:
                        print(f"\nDispositivo (Lote) atualmente instalado: {lote_instalado.to_string()}")
                    else:
                        print("\nNenhum dispositivo (lote) instalado neste veículo no momento.")

            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            #atualizar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("ATUALIZAR VEÍCULO")

            print("Selecione o veículo que deseja atualizar:")
            veiculos = ctrl_veiculo.listar_veiculos()
            veiculo_selecionado = ui_helper.selecionar_entidade(veiculos, "veículo")

            if veiculo_selecionado:
                print("\nDigite os novos dados (pressione Enter para manter o valor atual):")

                nova_placa = input(f"Nova placa ({veiculo_selecionado.get_placa()}): ").strip().upper()
                novo_frota = input(f"Novo código de frota ({veiculo_selecionado.get_frota() or ''}): ").strip()

                print("\nPara alterar a empresa proprietária, remova e cadastre o veículo novamente.")

                objeto_atualizado = False
                if nova_placa and len(nova_placa) == 7: # Valida formato
                    veiculo_selecionado.set_placa(nova_placa)
                    objeto_atualizado = True
                elif nova_placa: 
                    print("Formato de placa inválido, a placa não será alterada.")

                if novo_frota:
                    veiculo_selecionado.set_frota(novo_frota)
                    objeto_atualizado = True
                elif novo_frota == '': 
                    veiculo_selecionado.set_frota(None)
                    objeto_atualizado = True


                if objeto_atualizado:
                    if ui_helper.pedir_confirmacao("atualizar os dados deste veículo"):
                        if ctrl_veiculo.atualizar_veiculo(veiculo_selecionado):
                            print("\nVeículo atualizado com sucesso!")
                        else:
                            print("\nFalha ao atualizar veículo.")
                else:
                    print("\nNenhum dado válido alterado.")

            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            #remover
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REMOVER VEÍCULO")

            print("Selecione o veículo que deseja remover:")
            veiculos = ctrl_veiculo.listar_veiculos()
            veiculo_selecionado = ui_helper.selecionar_entidade(veiculos, "veículo")

            if veiculo_selecionado:
                acao = f"remover o veículo com placa '{veiculo_selecionado.get_placa()}'"
                if ui_helper.pedir_confirmacao(acao):
                    if ctrl_veiculo.remover_veiculo(veiculo_selecionado.get_id_veiculo()):
                        print("\nVeículo removido com sucesso!")

            input("\nPressione Enter para continuar...")
        elif opcao == '6':
            buscar_manutencao_interface()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENU DE GERENCIAMENTO DE DISPOSITIVOS
def menu_gerenciar_dispositivos(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_DISPOSITIVOS)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            #cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("CADASTRAR NOVO DISPOSITIVO (LOTE)")

            codigo = input("Digite o código do novo lote (Ex: LOT0001): ").strip().upper()
            obs = input("Digite uma observação (opcional): ").strip()

            if not codigo:
                print("\nErro: O código do lote é obrigatório.")
                input("\nPressione Enter para continuar...")
                return
            if len(codigo) > 7: 
                print("\nErro: O código do lote deve ter no máximo 7 caracteres.")
                input("\nPressione Enter para continuar...")
                return

            novo_lote_obj = Lot(id_lot=None,
                                codigo_lot=codigo,
                                obs_lot=obs if obs else None)

            if ui_helper.pedir_confirmacao(f"cadastrar o dispositivo com código '{codigo}'"):
                if ctrl_lote.inserir_lote(novo_lote_obj):
                    print("\nDispositivo cadastrado com sucesso!")
                else:
                    print("\nFalha ao cadastrar dispositivo.") 

            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #listar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE DISPOSITIVOS (LOTES)")

            lista_lotes = ctrl_lote.listar_lotes()

            if not lista_lotes:
                print("Nenhum dispositivo cadastrado.")
            else:
                print(f"{'ID':<5} | {'CÓDIGO':<10} | {'OBSERVAÇÃO':<40}")
                print("-" * 60)
                for lote in lista_lotes:
                    print(f"{lote.get_id_lot():<5} | {lote.get_codigo_lot():<10} | {(lote.get_obs_lot() or ''):<40}")

            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            #buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR DISPOSITIVO (LOTE) POR CÓDIGO")
            codigo_busca = input("Digite o código do lote a procurar: ").strip().upper()

            if not codigo_busca:
                print("Busca inválida. Por favor, digite um código.")
            else:
                lote_encontrado = ctrl_lote.buscar_lote_por_codigo(codigo_busca)

                if not lote_encontrado:
                    print(f"\nNenhum dispositivo encontrado com o código '{codigo_busca}'.")
                else:
                    print("\nDispositivo encontrado:")
                    print(lote_encontrado.to_string())

            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            #atualizar
            """ Orquestra o fluxo de atualização dos dados de um dispositivo (lote). """
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("ATUALIZAR DISPOSITIVO (LOTE)")

            print("Selecione o dispositivo que deseja atualizar:")
            lotes = ctrl_lote.listar_lotes()
            lote_selecionado = ui_helper.selecionar_entidade(lotes, "dispositivo")

            if lote_selecionado:
                print("\nDigite os novos dados (pressione Enter para manter o valor atual):")

                novo_codigo = input(f"Novo código ({lote_selecionado.get_codigo_lot()}): ").strip().upper()
                nova_obs = input(f"Nova observação ({lote_selecionado.get_obs_lot() or ''}): ").strip()

                objeto_atualizado = False
                if novo_codigo and len(novo_codigo) <= 7:
                    lote_selecionado.set_codigo_lot(novo_codigo)
                    objeto_atualizado = True
                elif novo_codigo:
                    print("Código inválido (máximo 7 caracteres), não será alterado.")

                if nova_obs:
                    lote_selecionado.set_obs_lot(nova_obs)
                    objeto_atualizado = True
                elif nova_obs == '': 
                    lote_selecionado.set_obs_lot(None)
                    objeto_atualizado = True

                if objeto_atualizado:
                    if ui_helper.pedir_confirmacao("atualizar os dados deste dispositivo"):
                        if ctrl_lote.atualizar_lote(lote_selecionado):
                            print("\nDispositivo atualizado com sucesso!")
                        else:
                            print("\nFalha ao atualizar dispositivo.")
                else:
                    print("\nNenhum dado válido alterado.")

            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            #remover
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REMOVER DISPOSITIVO (LOTE)")

            print("Selecione o dispositivo que deseja remover:")
            lotes = ctrl_lote.listar_lotes()
            lote_selecionado = ui_helper.selecionar_entidade(lotes, "dispositivo")

            if lote_selecionado:
                acao = f"remover o dispositivo com código '{lote_selecionado.get_codigo_lot()}'"
                if ui_helper.pedir_confirmacao(acao):
                    if ctrl_lote.remover_lote(lote_selecionado.get_id_lot()):
                        print("\nDispositivo removido com sucesso!")

            input("\nPressione Enter para continuar...")
        elif opcao == '6':
            #historico
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("HISTÓRICO DO DISPOSITIVO (LOTE)")

            print("Selecione o dispositivo para ver o histórico:")
            lotes = ctrl_lote.listar_lotes()
            lote_selecionado = ui_helper.selecionar_entidade(lotes, "dispositivo")

            if lote_selecionado:
                id_lote = lote_selecionado.get_id_lot()
                codigo_lote = lote_selecionado.get_codigo_lot()
                
                historico = ctrl_log.listar_log_por_lot(id_lote)
                
                ui_helper.limpar_tela()
                ui_helper.exibir_cabecalho(f"HISTÓRICO DO DISPOSITIVO: {codigo_lote}")

                if not historico:
                    print("Nenhum evento registrado para este dispositivo.")
                else:
                    print(f"{'ID':<5} | {'DATA':<12} | {'EVENTO':<25} | {'RESPONSÁVEL':<20} | {'VEÍCULO':<10} | {'EMPRESA':<20} | {'MANUT. ID':<10}")
                    print("-" * 110)
                    for evento in historico:
                        data_f = evento.get_data_evento().strftime('%d/%m/%Y') if evento.get_data_evento() else 'N/A'
                        cod_evento = evento.get_catalogo_eventos().get_codigo_evento() if evento.get_catalogo_eventos() else 'N/A'
                        resp = evento.get_responsavel_evento()
                        placa = evento.get_veiculo().get_placa() if evento.get_veiculo() else '-'
                        empresa = evento.get_empresa().get_nome_fantasia() if evento.get_empresa() else '-'
                        manut_id = evento.get_manutencao().get_id_manutencao() if evento.get_manutencao() else '-'
                        
                        print(f"{evento.get_id_log():<5} | {data_f:<12} | {cod_evento:<25} | {resp:<20} | {placa:<10} | {empresa:<20} | {manut_id:<10}")

            input("\nPressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENU DE GERENCIAMENTO DE USUÁRIOS
def menu_editar_usuarios(usuario_logado: Usuario):
    """ Menu para as ações de edição de um usuário. """
    while True:
        ui_helper.limpar_tela()
        print(MENU_EDITAR_USUARIOS)
        opcao_edicao = input("Escolha uma opção: ")
        ui_helper.limpar_tela()
        ui_helper.exibir_cabecalho("ATUALIZAR USUÁRIO")
        
        print("Selecione o usuário que deseja atualizar:")
        usuarios = ctrl_usuario.listar_todos_usuarios()
        usuario_selecionado = ui_helper.selecionar_entidade(usuarios, "usuário")

        if opcao_edicao == '1':
            #atualizar
            print("\nDigite os novos dados (pressione Enter para manter o valor atual):")
            novo_nome = input(f"Novo nome completo ({usuario_selecionado.get_nome_completo()}): ").strip()
            novo_email = input(f"Novo e-mail ({usuario_selecionado.get_email_usuario()}): ").strip()
            nova_senha = input("Nova senha (deixe em branco para não alterar): ")

            objeto_atualizado = False
            if novo_nome:
                usuario_selecionado.set_nome_completo(novo_nome)
                objeto_atualizado = True
            if novo_email:
                usuario_selecionado.set_email_usuario(novo_email)
                objeto_atualizado = True
            if nova_senha:
                usuario_selecionado.set_senha(nova_senha)
                objeto_atualizado = True

            if objeto_atualizado:
                if ui_helper.pedir_confirmacao("atualizar os dados deste usuário"):
                    if ctrl_usuario.atualizar_usuario(usuario_selecionado):
                        print("\nUsuário atualizado com sucesso!")
                    else:
                        print("\nFalha ao atualizar usuário.")
            else:
                print("\nNenhum dado alterado.")    
            input("\nPressione Enter para continuar...")

        elif opcao_edicao == '2':
            if usuario_selecionado is usuario_logado:
                print("Você não pode remover o usuário que está logado.")
            else:
                acao = f"remover o usuário '{usuario_selecionado.get_nome_completo()}'"
                if ui_helper.pedir_confirmacao(acao):
                    if ctrl_usuario.remover_usuario(usuario_selecionado.get_id_usuario()):
                        print("\nUsuário removido com sucesso!")
                    else:
                        print("\nFalha ao remover usuário.")
            input("\nPressione Enter para continuar...")
        elif opcao_edicao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

def menu_gerenciar_usuarios(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_USUARIOS) 
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            #cadastrar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("CADASTRAR NOVO USUÁRIO")
            
            nome = input("Digite o nome completo: ").strip()
            email = input("Digite o e-mail (será o login): ").strip()
            senha = input("Digite a senha: ")

            if not nome or not email or not senha:
                print("\nErro: Nome, e-mail e senha são obrigatórios!")
                input("\nPressione Enter para continuar...")
                return
            
            novo_usuario_obj = Usuario(id_usuario=None, 
                                    nome_completo=nome, 
                                    email_usuario=email, 
                                    senha=senha) 
            if ui_helper.pedir_confirmacao(f"cadastrar o usuário '{nome}'"):
                if ctrl_usuario.inserir_usuario(novo_usuario_obj):
                    print("\nUsuário cadastrado com sucesso!")
                else:
                    print("\nFalha ao cadastrar usuário.")
                    
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #listar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("LISTA DE USUÁRIOS")

            lista_usuarios = ctrl_usuario.listar_todos_usuarios()
            
            if not lista_usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                print(f"{'ID':<5} | {'NOME COMPLETO':<40} | {'E-MAIL (LOGIN)':<30}")
                print("-" * 80)
                for usuario in lista_usuarios:
                    print(f"{usuario.get_id_usuario():<5} | {usuario.get_nome_completo():<40} | {usuario.get_email_usuario():<30}")

            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            #buscar
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("BUSCAR USUÁRIO")
            
            termo_busca = input("Digite o nome ou e-mail do usuário a procurar: ")
            
            if not termo_busca.strip():
                print("Busca inválida.")
            else:
                usuario_por_email = ctrl_usuario.buscar_usuario_por_email(termo_busca)
                if usuario_por_email:
                    print("\nUsuário encontrado por e-mail:")
                    print(usuario_por_email.to_string())
                else:
                    lista_resultado_nome = ctrl_usuario.buscar_usuario_por_nome(termo_busca)
                    if not lista_resultado_nome:
                        print(f"\nNenhum usuário encontrado com o termo '{termo_busca}'.")
                    else:
                        print("\nUsuários encontrados por nome:")
                        for usuario in lista_resultado_nome:
                            print(usuario.to_string())
                            
            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            menu_editar_usuarios(usuario_logado)
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            input("\nPressione Enter para continuar...")

# MENU DE GERENCIAMENTO DE ENTIDADES
def menu_gerenciar_entidades(usuario_logado: Usuario):
    while True:
        ui_helper.limpar_tela()
        print(MENU_GERENCIAR_ENTIDADES)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciar_empresas()
        elif opcao == '2':
            menu_gerenciar_contatos()
        elif opcao == '3':
            menu_gerenciar_tecnicos()
        elif opcao == '4':
            menu_gerenciar_veiculos()
        elif opcao == '5':
            menu_gerenciar_dispositivos()
        elif opcao == '6':
            menu_gerenciar_usuarios()
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

        if opcao == '1':
            #nova visita
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REGISTRAR NOVA VISITA TÉCNICA")

            print("Selecione o técnico que realizou a visita:")
            nome_tecnico = input("Digite o nome do técnico: ")
            tecnicos_encontrados = ctrl_tecnico.buscar_tecnicos_por_nome(nome_tecnico)
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_encontrados, "técnico")

            if not tecnico_selecionado:
                input("\nPressione Enter para continuar...")
                return

            data_visita = date.today()
            print(f"Data da visita registrada como: {data_visita.strftime('%d/%m/%Y')}")

            nova_visita_obj = VisitaTecnica(id_visita=None, tecnico=tecnico_selecionado, data_visita=data_visita)

            if ui_helper.pedir_confirmacao(f"registrar visita para '{tecnico_selecionado.get_contato().get_nome_contato()}' em {data_visita.strftime('%d/%m/%Y')}"):
                if ctrl_visita.inserir_visita(nova_visita_obj):
                    print("\nVisita técnica registrada com sucesso!")
                else:
                    print("\nFalha ao registrar visita técnica.")

            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            #novo defeito
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REGISTRAR NOVO DEFEITO EM VEÍCULO")

            placa = input("Digite a placa do veículo que apresentou o defeito: ").strip().upper()
            veiculo_selecionado = ctrl_veiculo.buscar_veiculo_por_placa(placa)

            if not veiculo_selecionado:
                print(f"Veículo com a placa '{placa}' não encontrado.")
                input("\nPressione Enter para continuar...")
                return

            print(f"\nVeículo selecionado: {veiculo_selecionado.to_string()}")

            print("\nSelecione o tipo de defeito:")
            lista_defeitos_catalogo = ctrl_cat_defeitos.listar_defeitos()
            catalogo_defeito_selecionado = ui_helper.selecionar_entidade(lista_defeitos_catalogo, "tipo de defeito")

            if not catalogo_defeito_selecionado:
                input("\nPressione Enter para continuar...")
                return

            data_reporte = date.today() 
            status_defeito = "ABERTO" 
            obs_defeitos = input("Digite observações sobre o defeito (opcional): ").strip()

            novo_defeito_obj = Defeito(id_defeito=None,
                                    catalogo_defeito=catalogo_defeito_selecionado,
                                    veiculo=veiculo_selecionado,
                                    data_reporte=data_reporte,
                                    status_defeito=status_defeito,
                                    obs_defeitos=obs_defeitos if obs_defeitos else None)

            if ui_helper.pedir_confirmacao("registrar este defeito"):
                if ctrl_defeito.inserir_defeito(novo_defeito_obj):
                    print("\nDefeito registrado com sucesso!")
                else:
                    print("\nFalha ao registrar o defeito.")

            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            #nova manutencao
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REGISTRAR NOVA MANUTENÇÃO")

            print("Selecione o técnico que realizou a visita:")
            nome_tecnico = input("Digite o nome do técnico: ")
            tecnicos_encontrados = ctrl_tecnico.buscar_tecnicos_por_nome(nome_tecnico) # Busca apenas ativos por padrão
            tecnico_selecionado = ui_helper.selecionar_entidade(tecnicos_encontrados, "técnico")

            if not tecnico_selecionado:
                input("\nPressione Enter para continuar...")
                return

            data_visita = date.today() 
            print(f"\nRegistrando visita técnica para {tecnico_selecionado.get_contato().get_nome_contato()} em {data_visita.strftime('%d/%m/%Y')}")
            nova_visita_obj = VisitaTecnica(id_visita=None, tecnico=tecnico_selecionado, data_visita=data_visita)
            if not ctrl_visita.inserir_visita(nova_visita_obj):
                print("\nFalha ao registrar a visita técnica. Abortando a manutenção.")
                input("\nPressione Enter para continuar...")
                return

            visitas_do_tecnico = ctrl_visita.buscar_visita_por_tecnico(tecnico_selecionado.get_id_tecnico())
            if not visitas_do_tecnico:
                print("\nErro crítico: Não foi possível recuperar a visita recém-criada.")
                input("\nPressione Enter para continuar...")
                return
            visita_registrada = visitas_do_tecnico[0] 

            placa = input("\nDigite a placa do veículo que recebeu a manutenção: ").strip().upper()
            veiculo = ctrl_veiculo.buscar_veiculo_por_placa(placa)
            if not veiculo:
                print(f"Veículo com a placa '{placa}' não encontrado.")
                input("\nPressione Enter para continuar...")
                return

            defeitos_do_veiculo = ctrl_defeito.listar_defeitos_em_veiculo(veiculo.get_id_veiculo())
            defeitos_em_aberto = [d for d in defeitos_do_veiculo if d.get_status_defeito() == 'ABERTO']

            if not defeitos_em_aberto:
                print(f"\nNenhum defeito em aberto encontrado para o veículo {placa}.")
                input("\nPressione Enter para continuar...")
                return

            print("\nSelecione o defeito que foi corrigido:")
            defeito_selecionado = ui_helper.selecionar_entidade(defeitos_em_aberto, "defeito")

            if not defeito_selecionado:
                input("\nPressione Enter para continuar...")
                return

            print("\nSelecione a ação que foi realizada:")
            acoes_catalogo = ctrl_cat_acoes.listar_acoes()
            acao_selecionada = ui_helper.selecionar_entidade(acoes_catalogo, "ação")

            if not acao_selecionada:
                input("\nPressione Enter para continuar...")
                return

            obs_servico = input("Digite as observações do serviço (opcional): ").strip()

            nova_manutencao_obj = Manutencao(id_manutencao=None,
                                            visita=visita_registrada,
                                            catalogo_acao=acao_selecionada,
                                            defeito=defeito_selecionado,
                                            obs_servico=obs_servico if obs_servico else None)

            if ui_helper.pedir_confirmacao("registrar esta manutenção"):
                if ctrl_manutencao.inserir_manutencao(nova_manutencao_obj):
                    print("\nManutenção registrada com sucesso!")
                    defeito_selecionado.set_status_defeito('FECHADO')
                    if ctrl_defeito.atualizar_defeito(defeito_selecionado):
                        print(f"Status do defeito ID {defeito_selecionado.get_id_defeito()} atualizado para 'FECHADO'.")
                    else:
                        print(f"ATENÇÃO: Falha ao atualizar o status do defeito ID {defeito_selecionado.get_id_defeito()}. Faça isso manualmente.")
                else:
                    print("\nFalha ao registrar a manutenção.")

            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            #novo evento
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("REGISTRAR EVENTO NO HISTÓRICO DO LOT")

            codigo_lote = input("Digite o código do Lote (Dispositivo): ").strip().upper()
            lote_selecionado = ctrl_lote.buscar_lote_por_codigo(codigo_lote)
            if not lote_selecionado:
                print(f"Lote com código '{codigo_lote}' não encontrado.")
                input("\nPressione Enter para continuar...")
                return
            print(f"Dispositivo selecionado: {lote_selecionado.to_string()}")

            print("\nSelecione o tipo de evento:")
            eventos_catalogo = ctrl_cat_eventos.listar_eventos()
            evento_selecionado = ui_helper.selecionar_entidade(eventos_catalogo, "tipo de evento")
            if not evento_selecionado:
                input("\nPressione Enter para continuar...")
                return

            veiculo_selecionado = None
            empresa_selecionada = None
            manutencao_selecionada = None

            if evento_selecionado.get_codigo_evento() in ['INSTALACAO', 'DESINSTALACAO']:
                placa_veiculo = input("Digite a placa do veículo associado ao evento: ").strip().upper()
                veiculo_selecionado = ctrl_veiculo.buscar_veiculo_por_placa(placa_veiculo)
                if not veiculo_selecionado:
                    print(f"Veículo com placa '{placa_veiculo}' não encontrado.")
                    break
           
            if evento_selecionado.get_codigo_evento() == 'TRANSFERENCIA_UNIDADE':
                nome_empresa = input("Digite o nome da empresa de destino: ")
                empresas_encontradas = ctrl_empresa.buscar_empresa_por_nome(nome_empresa)
                empresa_selecionada = ui_helper.selecionar_entidade(empresas_encontradas, "empresa de destino")
            
            

            data_evento = date.today()
            obs_evento = input("Digite observações sobre o evento (opcional): ").strip()
            responsavel_evento = usuario_logado.get_nome_completo() 

            novo_log_obj = LogLot(id_log=None,
                                lote=lote_selecionado,
                                veiculo=veiculo_selecionado,
                                empresa=empresa_selecionada,
                                manutencao=manutencao_selecionada,
                                catalogo_eventos=evento_selecionado,
                                data_evento=data_evento,
                                responsavel_evento=responsavel_evento,
                                obs_evento=obs_evento if obs_evento else None)

            if ui_helper.pedir_confirmacao(f"registrar o evento '{evento_selecionado.get_codigo_evento()}' para o lote '{lote_selecionado.get_codigo_lot()}'"):
                if ctrl_log.inserir_log(novo_log_obj):
                    print("\nEvento registrado no histórico com sucesso!")
                else:
                    print("\nFalha ao registrar evento.")

            input("\nPressione Enter para continuar...")
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

        #relatorio detalhado em uma empresa x
        elif opcao == '4':
            ui_helper.limpar_tela()
            ui_helper.exibir_cabecalho("RELATÓRIO DETALHADO POR EMPRESA")

            nome_busca = input("Digite o nome da empresa: ")
            empresas_encontradas = ctrl_empresa.buscar_empresa_por_nome(nome_busca)
            empresa_selecionada = ui_helper.selecionar_entidade(empresas_encontradas, "empresa") 

            if empresa_selecionada:
                id_empresa = empresa_selecionada.get_id_empresa()
                nome_empresa = empresa_selecionada.get_nome_fantasia()
                
                dados_relatorio = relatorios_manager.get_relatorio_detalhado_empresa(id_empresa)

                ui_helper.limpar_tela()
                ui_helper.exibir_cabecalho(f"RELATÓRIO DETALHADO: {nome_empresa.upper()}")
                
                print("\n--- DEFEITOS ATUAIS EM ABERTO ---")
                if dados_relatorio and "defeitos_atuais" in dados_relatorio and dados_relatorio["defeitos_atuais"]:
                    print(f"  {'PLACA':<10} | {'DATA REPORTE':<12} | {'DESCRIÇÃO':<40}")
                    print("  " + "-" * 65)
                    for defeito in dados_relatorio["defeitos_atuais"]:
                        data_formatada = defeito['data_reporte'].strftime('%d/%m/%Y') if defeito['data_reporte'] else 'N/A'
                        print(f"  {defeito['placa']:<10} | {data_formatada:<12} | {defeito['descricao']:<40}")
                else:
                    print("  Nenhum defeito em aberto para os veículos desta empresa.")

                print("\n--- VEÍCULOS DA FROTA ---")
                if dados_relatorio and "veiculos" in dados_relatorio and dados_relatorio["veiculos"]:
                    print(f"  {'PLACA':<10} | {'FROTA':<15}")
                    print("  " + "-" * 28)
                    for veiculo in dados_relatorio["veiculos"]:
                        print(f"  {veiculo['placa']:<10} | {(veiculo['frota'] or ''):<15}")
                else:
                    print("  Nenhum veículo cadastrado.")

                print("\n--- TÉCNICOS ASSOCIADOS ---")
                if dados_relatorio and "tecnicos" in dados_relatorio and dados_relatorio["tecnicos"]:
                    print(f"  {'NOME':<30} | {'LOCAL':<20}")
                    print("  " + "-" * 53)
                    for tecnico in dados_relatorio["tecnicos"]:
                        print(f"  {tecnico['nome']:<30} | {tecnico['local']:<20}")
                else:
                    print("  Nenhum técnico associado.")

                print("\n--- HISTÓRICO DE MANUTENÇÕES REALIZADAS ---")
                if dados_relatorio and "manutencoes" in dados_relatorio and dados_relatorio["manutencoes"]:
                    print(f"  {'DATA':<12} | {'PLACA':<10} | {'DEFEITO':<30} | {'TÉCNICO':<25}")
                    print("  " + "-" * 82)
                    for manutencao in dados_relatorio["manutencoes"]:
                        data_formatada = manutencao['data'].strftime('%d/%m/%Y') if manutencao['data'] else 'N/A'
                        defeito_desc = (manutencao['defeito'][:27] + '...') if manutencao['defeito'] and len(manutencao['defeito']) > 30 else (manutencao['defeito'] or '') 
                        print(f"  {data_formatada:<12} | {manutencao['placa']:<10} | {defeito_desc:<30} | {manutencao['tecnico']:<25}")
                else:
                    print("  Nenhum registro de manutenção encontrado.")

            input("\nPressione Enter para voltar...")
        #voltar
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")


def menu_principal(usuario_logado: Usuario):
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