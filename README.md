# Sistema de Controle de Manutenção e Ativos

Este sistema simula uma aplicação real para gerenciar a manutenção de veículos de frota, o ciclo de vida de dispositivos rastreadores (lots) e o controle de acesso de usuários. O sistema utiliza Python para a interface e lógica de aplicação, e Oracle como Sistema de Gerenciamento de Banco de Dados.

## Pré-requisitos

* Python 3.x
* Oracle (recomenda-se a versão Express Edition - XE)
* Bibliotecas Python listadas no arquivo `requirements.txt`.

## Configuração do Ambiente (Passos Únicos)

Antes de executar a aplicação pela primeira vez, é necessário configurar o usuário no banco de dados Oracle e criar a estrutura de tabelas.

### 1. Configuração do Usuário no Oracle

Este passo deve ser realizado **uma única vez**.

1.  Conecte-se à sua instância Oracle via DBeaver utilizando um usuário com privilégios de administrador (ex: `SYSTEM`).
2.  Crie o usuário que será o "dono" dos objetos do projeto (tabelas, sequences, etc.). **Substitua `seu_usuario` e `sua_senha` por credenciais de sua escolha.**

    ```sql
    -- 1. Cria o usuário do projeto
    CREATE USER seu_usuario IDENTIFIED BY sua_senha;

    -- 2. Concede as permissões essenciais de conexão e criação de objetos
    GRANT CONNECT, RESOURCE TO seu_usuario;

    -- 3. Concede a cota de armazenamento (crucial para evitar o erro ORA-01950)
    ALTER USER seu_usuario QUOTA UNLIMITED ON USERS;
    ```

### 2. Configuração das Credenciais na Aplicação

1.  Navegue até a pasta `src/conexion/passphrase/`.
2.  Crie um arquivo de texto chamado `authentication.oracle`.
3.  Dentro deste arquivo, escreva o nome de usuário e a senha que você criou no passo anterior, separados por uma vírgula, sem espaços. Exemplo:
    `projetodados,minhasenha123`
4.  **OBS:** O arquivo `.gitignore` já está configurado para **não** enviar esta pasta para o GitHub.

### 3. Instalação das Dependências Python

Abra um terminal na pasta raiz do projeto e execute o seguinte comando para instalar a biblioteca necessária:

```bash
pip install -r requirements.txt
```

### 4. Criação da Estrutura do Banco de Dados

Com o usuário criado e as dependências instaladas, execute o script Python que criará todas as tabelas, sequences e relacionamentos automaticamente:

```bash
python setup_database.py
```

## Execução do Projeto

Após a configuração inicial do banco de dados, para executar o sistema principal, utilize o comando a partir da pasta raiz do projeto:

```bash
python principal.py
```
O sistema exibirá a tela de login. Utilize o usuário Administrador Padrão (Email: `admin@sistema.com` | Senha: `senha123`) ou um usuário que você tenha cadastrado.

## Organização do Projeto

[cite_start]O projeto segue a estrutura modular sugerida no edital[cite: 133]:

* [cite_start]**diagrams:** Contém o diagrama relacional do banco de dados nos formatos `.architect` (SQL Power Architect) e `.pdf`[cite: 114].
* [cite_start]**sql:** Armazena os scripts SQL[cite: 136].
    * [cite_start]`main.sql`: Script mestre para criação de todas as tabelas, sequences e relacionamentos[cite: 112].
    * `insert_samples_base.sql`: Script para popular as tabelas de cadastro e catálogo com dados de exemplo.
    * `insert_samples_related.sql`: Script com blocos PL/SQL para popular as tabelas de transação com dados de exemplo relacionados.
* [cite_start]**src:** Contém o código-fonte Python da aplicação[cite: 113].
    * [cite_start]**conexion:** Módulo responsável pela conexão com o banco de dados Oracle[cite: 135, 139].
    * [cite_start]**controller:** Classes controladoras que implementam a lógica de negócio e as operações CRUD, fazendo a ponte entre o `model` e o `conexion`[cite: 141, 144, 145].
    * [cite_start]**model:** Classes que representam as 15 entidades do diagrama relacional (tabelas)[cite: 134, 137, 138].
    * [cite_start]**reports:** Módulo responsável por gerar os relatórios solicitados, buscando e formatando os dados[cite: 143, 147].
    * [cite_start]**utils:** Módulos auxiliares[cite: 142, 146].
        * `config.py`: Define as strings de texto dos menus da aplicação.
        * `splash_screen.py`: Controla a exibição da tela de abertura.
        * `ui_helpers.py`: Contém funções para interações comuns com o usuário (limpar tela, selecionar entidade, pedir confirmação).
* [cite_start]**principal.py:** Script principal que inicializa a aplicação, gerencia o fluxo de menus e une todos os módulos[cite: 148, 149].
* **setup_database.py:** Script utilitário para automatizar a criação da estrutura do banco de dados a partir do `main.sql`.
* **requirements.txt:** Lista as bibliotecas Python necessárias para o projeto.
* [cite_start]**README.md:** Este arquivo, contendo a documentação do projeto[cite: 118].

## Bibliotecas Utilizadas

* **oracledb:** Driver oficial da Oracle para conexão Python com o banco de dados.

## Troubleshooting (Solução de Problemas Comuns)

* **`ORA-01017: invalid username/password`**: Verifique se o usuário e senha no arquivo `src/conexion/passphrase/authentication.oracle` correspondem exatamente aos criados no Oracle.
* **`ORA-12514: TNS:listener does not currently know of service requested`**: Confira o `_service_name` (geralmente `XEPDB1` ou `XE`) na classe `OracleDB` (`src/conexion/oracle_db.py`). Verifique também se os serviços do Oracle estão rodando na sua máquina (`services.msc` no Windows).
* **`ORA-01950: no privileges on tablespace 'USERS'`**: O usuário do projeto não tem permissão para usar espaço em disco. Execute `ALTER USER seu_usuario QUOTA UNLIMITED ON USERS;` com o usuário `SYSTEM`.
* **`ORA-00900: invalid SQL statement`**: Geralmente causado por tentar executar um comando PL/SQL (`DECLARE...BEGIN...END;`) como se fosse SQL simples, ou por um erro de sintaxe (como falta de `;`). Execute blocos PL/SQL como "Script" (`Alt+X` no DBeaver, `F5` no SQL Developer) ou remova o `/` final.
* **`ORA-01403: no data found`**: Ocorre em blocos PL/SQL quando um `SELECT INTO` não encontra a linha esperada. Verifique se os dados de referência (nos scripts `insert_samples_base`) foram inseridos corretamente antes de rodar os scripts relacionados.
* **`ImportError: cannot import name ...` / `ModuleNotFoundError`**: Verifique se a estrutura de pastas está correta, se todos os arquivos `__init__.py` necessários existem e se você está executando os scripts Python a partir da pasta raiz do projeto.

## [cite_start]Entregáveis

Este repositório contém:
* [cite_start]✅ Script de criação das tabelas e relacionamentos (`sql/main.sql`)[cite: 112].
* ✅ Código fonte do programa desenvolvido, organizado em diretórios (`src/`, `principal.py`, etc.)[cite: 113].
* [cite_start]✅ Diagrama relacional (`diagrams/`)[cite: 114].
* [cite_start]✅ Vídeo demonstrativo (Link a ser inserido aqui)[cite: 115].
* ✅ Este arquivo `README.MD` explicando como executar o projeto[cite: 118].

## Equipe
* **Componentes:**
    * Isabella M.
* **Disciplina:** Banco de Dados
* **Professor:** Howard Roatti

