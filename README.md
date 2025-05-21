# Favorite API

## Instruções para uso

### 1. Criação do arquivo .env
É necessário criar um arquivo .env com algumas credenciais. No repositorio já existe o arquivo **local.env** com as variaveis que são necessárias, bastanto copia-las para seu arquivo .env e adicionar seus respctivos valores.

Exemplo de como deve ficar seu arquivo *.env*:
```shell
POSTGRES_SERVER=favorite_api
POSTGRES_PORT=5432
POSTGRES_USER=root
POSTGRES_PASSWORD=12345
POSTGRES_DB=favorites_db

FIRST_SUPERUSER=root@gmail.com
FIRST_SUPERUSER_PASSWORD=12345

REDIS_HOST=redis
REDIS_PORT=6379
```

### 2. Construir a imagem e subir a API
```shell
docker-compose up --build
```

A API ficará disponivel em: http://localhost:5000/docs

**Acesso:**
Inicialmente vai ser criado um usuário com email e senha definidos dentro do **.env**. Esse usuário deve ser utilizado para criar outros usuários.

### 3. Rodar os testes
```shell
docker compose run unit-tests
```