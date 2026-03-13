# 🏫 API de Gestão Escolar - IBMEC 2026.1

Esta API foi desenvolvida para automatizar a gestão de alunos e seus respectivos endereços. O sistema utiliza o framework FastAPI e integra-se à API externa **ViaCEP** para buscar informações de endereçamento automaticamente a partir do CEP, persistindo os dados em um banco de dados MySQL.

## 🚀 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**: Criação das rotas e lógica da API.
* **Pandas**: Processamento de dados e interface simplificada com o banco.
* **SQLAlchemy & PyMySQL**: Comunicação com o servidor MySQL.
* **Requests**: Consumo da API ViaCEP.
* **Uvicorn**: Servidor ASGI para rodar a aplicação.

## 🛠️ Configuração e Instalação

### 1. Requisitos
Certifique-se de ter o **MySQL** instalado e rodando em sua máquina, além do Python 3.

### 2. Instalação de Dependências
No terminal, dentro da pasta do projeto, execute:
```bash
pip install -r requirements.txt

3. Banco de Dados

O projeto utiliza um banco de dados chamado db_escola. Certifique-se de executar o script SQL contido no arquivo sql_basico.sql para criar as tabelas tb_alunos, tb_enderecos e a view vw_alunos_enderecos.

4. Execução
Para iniciar o servidor, utilize o comando:

Bash

uvicorn main:app --reload
A API estará disponível em: http://127.0.0.1:8000

📌 Documentação dos EndpointsAbaixo, os principais recursos disponíveis na API:MétodoEndpointDescriçãoGET/alunos/Retorna a lista de todos os alunos cadastrados.GET/enderecos/Retorna a lista de todos os endereços salvos.GET/enderecos-alunos/Retorna a junção de alunos e endereços (via View).POST/cadastrar-endereco-cep/{cep}Consulta o ViaCEP e cadastra o endereço no banco.POST/cadastrar-aluno/Cadastra um novo aluno (recebe JSON).PUT/atualizar-alunos/{id}Atualiza os dados de um aluno pelo ID.DELETE/deletar-alunos/{id}Remove um aluno do banco de dados.👨‍💻 AutorDesenvolvido por Bruno Augusto como projeto para a disciplina de Ciência de Dados.
---

### Bônus: Arquivo `requirements.txt`
Caso você ainda não tenha criado, este é o conteúdo que deve estar no seu arquivo `requirements.txt` para que o comando de instalação do README funcione:

```text
fastapi
uvicorn
pandas
requests
sqlalchemy
pymysql
cryptography