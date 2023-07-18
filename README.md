# Weather Project

## Visão Geral

O Weather Project é um serviço de informações climáticas que fornece dados sobre o clima de várias cidades. Foi desenvolvido com foco no Domain-Driven Design (DDD) e usa uma arquitetura Onion para uma estrutura de software robusta e bem organizada.

## Tecnologias Utilizadas

* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
  * [Motor](https://motor.readthedocs.io/)
* [Docker](https://www.docker.com/)

## Arquitetura do Projeto

Utilizamos Domain-Driven Design (DDD) e a Arquitetura Onion para criar uma aplicação resiliente e bem estruturada, onde todas as partes essenciais estão localizadas no núcleo da aplicação. Isso garante que a troca de detalhes de infraestrutura não afete as regras e a lógica do negócio.

A estrutura de diretórios é a seguinte:

```tree
├── app
│   ├── application
│   │   └── adapters
│   │   └── errors
│   │   └── extensions
│   │   └── helpers
│   ├── domain
│   │   └── interfaces.py
│   │   └── constants.py
│   │   └── models
│   │   └── services
│   ├── infrastructure
│   │   └── db
│   │   └── repositories
│   │   └── schemas
│   ├── presentation
│   │   └── views
│   ├── main.py
│   ├── config.py
└── tests
```

Para mais detalhes sobre o que cada camada faz, confira nossa [documentação de arquitetura](https://github.com/ylgnerbecton/weather-journey/wiki/Documenta%C3%A7%C3%A3o-de-Arquitetura).

## Como começar

### Executar aplicação com Docker

Nesta aplicação, três imagens Docker serão criadas:

- app_weather: Esta é a imagem Docker da aplicação FastApi.
- db_weather: Esta é a imagem Docker para o banco de dados MongoDB.
- weather_bot_telegram: Esta imagem Docker é usada para inicializar o bot do Telegram.

Siga as instruções abaixo para executar a aplicação:


1. Crie um arquivo .env local copiando o conteúdo do arquivo sample.env:
```
cp example.env .env
```

2. Inicie a aplicação com Docker:

```bash
make start-build
```

### Como utlizar a aplicação

1. Após a aplicação ser iniciada com Docker, você pode visualizar os serviços disponíveis através do Swagger:
    http://localhost:8010/docs/


2. Use a API para pesquisar informações sobre o clima de uma cidade:

```
  curl -X 'POST' \
  'http://localhost:8010/api/v1/local-weather' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Campinas"
  }'
```

3. Você também pode interagir com a aplicação através do nosso bot do Telegram, @weather_tetris_bot. Basta enviar o comando /start e inserir o nome da cidade após o bot estar ativado.

### Como executar testes unitários

Execute os testes unitários com o seguinte comando:
```bash
make test
```
