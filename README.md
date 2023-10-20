### ETL e Análise dos Dados do Portal da Transparência da Emurb
***

#### Requisitos para o projeto:
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
***

#### Executando o ETL:

No diretório raiz do projeto execute:
* `docker-compose up -d`
    &nbsp;
    Isso será suficiente para que seja criado um conteiner com um banco de dados PostgreSQL e um serviço que execute scripts Python.
    &nbsp;
    Os scripts `.py` que serão executados são responsáveis por fazer a transformação e o carregamento dos dados nas tabelas do banco.
    &nbsp;
***

#### Fazendo consultas no banco de dados
Caso deseje realizar consultas SQL após o carregamento dos dados, execute:
* `docker exec -it postgres psql -U postgres`
* `\c datawarehouse`
    &nbsp;
    Isso abrirá uma conexão com o banco de dados e permitirá as consultas.

Para sair do console PostgreSQL, execute:
* `\q`