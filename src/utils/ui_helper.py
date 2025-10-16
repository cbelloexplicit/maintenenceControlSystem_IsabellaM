import os

def limpar_tela():
    """
    Limpa a tela do console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def selecionar_entidade(lista_entidades: list, prompt_singular: str) -> any:
    """
    Função genérica para exibir uma lista de objetos, permitir que o usuário escolha um e retornar o objeto selecionado.
    """
    if not lista_entidades:
        print(f"\nNenhum(a) {prompt_singular} encontrado(a).")
        return None

    print(f"\n{prompt_singular.capitalize()}s encontrados:")
    for i, entidade in enumerate(lista_entidades):
        print(f"  {i + 1} - {entidade.to_string()}")

    while True:
        try:
            escolha = int(input(f"\nDigite o número do(a) {prompt_singular} desejado(a) (ou 0 para cancelar): "))

            if escolha == 0:
                print("Operação cancelada.")
                return None

            if 1 <= escolha <= len(lista_entidades):
                # Retorna o objeto inteiro que foi escolhido
                return lista_entidades[escolha - 1]
            else:
                print("Número inválido. Por favor, escolha um número da lista.")

        except ValueError:
            print("Entrada inválida. Por favor, digite apenas o número.")


def pedir_confirmacao(acao: str) -> bool:
    """
    Exibe uma mensagem de confirmação para o usuário.
    """
    while True:
        confirmacao = input(f"Tem certeza que deseja {acao} (S/N)? ").strip().upper()
        if confirmacao in ['S', 'N']:
            return confirmacao == 'S'
        else:
            print("Opção inválida. Por favor, digite 'S' para sim ou 'N' para não.")


def exibir_cabecalho(titulo: str):
    """
    Exibe um cabeçalho formatado para os menus.
    """
    print("\n" + "=" * 30)
    print(f"  {titulo.upper()}")
    print("=" * 30)