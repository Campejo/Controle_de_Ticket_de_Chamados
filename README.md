# Gerenciador de Chamados - Protótipo

## Descrição
Este projeto é um protótipo de um sistema de gerenciamento de chamados desenvolvido em Python. Ele permite o controle de tickets, incluindo a criação, edição, finalização e remoção de chamados, utilizando um banco de dados PostgreSQL.

## Tecnologias Utilizadas
- **Python**
- **PostgreSQL**
- **psycopg2** (biblioteca para interação com o banco de dados)
- **dotenv** (para carregamento de variáveis de ambiente)
- **Tkinter** (para interface gráfica)

## Estrutura do Projeto

```
/
|-- project/
|   |-- Main.py      # Arquivo principal do sistema
|   |-- DB/
|   |   |-- AppDB.py # Classe de conexão e manipulação do banco de dados
|-- .env             # Configuração das credenciais do banco de dados
|-- README.md        # Este arquivo
```

## Funcionalidades Principais
### `AppDB.py`
A classe `AppDB` gerencia a conexão com o banco de dados e fornece os seguintes métodos:
- **abrirConexao()**: Estabelece conexão com o PostgreSQL.
- **fecharConexao()**: Fecha a conexão com o banco.
- **selecionarDados()**: Retorna todos os chamados registrados no sistema.
- **inserirChamado(id, local, descricao, abertura)**: Registra um novo chamado na base de dados.
- **atualizarChamado(id, local_novo, descricao_nova)**: Modifica os atributos de um chamado existente.
- **finalizarChamado(id)**: Insere a data de encerramento de um chamado específico.
- **deletarChamado(id)**: Remove um chamado definitivamente do banco de dados.

### `Main.py`
Arquivo principal onde a lógica do sistema é implementada, utilizando a classe `AppDB` para manipulação dos chamados.

## Configuração e Execução
1. **Instalar dependências**
   ```bash
   pip install psycopg2 python-dotenv
   ```
2. **Configurar variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto e defina:
   ```env
   DB_NAME=seu_banco
   DB_USER=seu_usuario
   DB_HOST=seu_host
   DB_PASSWORD=sua_senha
   ```
3. **Executar o sistema**
   ```bash
   python project/Main.py
   ```

## Possíveis Melhorias
- Melhorar a interface gráfica utilizando Tkinter.
- Melhorar o tratamento de erros nas conexões com o banco.
- Criar testes automatizados para validação das funcionalidades.

## Autor
Desenvolvido por [ Thiago Campello ] como parte de um projeto de extensão.
