# ams
Athletic Management System

## Helpers

### Docker
Usando docker para fazer com que systema rode em qualquer systema operacional sem fazer nenhuma modificação

[Instalar o docker](https://docs.docker.com/install/)

#### Build docker

docker-compose build

### Travis-CI
Travis-CI para não deixaro systema ser upado para o git se ouver erros

### TDD (Test-driven development)
A metodologia se baseia em criar testes antes de criar o codigo para ter mais comfiabilidade que o test não foi fetio para passar no codigo.

## RUN

O sistema está na porta 8000, quando acessar use localhost:8000

The application port is 8000, always remember to go to localhost:8000 to access the application

### Tests

To run the tests use:
docker-compose run --rm ams sh -c "python manage.py test && flake8"

### Application

To run the application use:
docker-compose up

## Paths

Disponivel até o moento

http://localhost:8000/api/user/create/
http://localhost:8000/api/user/token/
