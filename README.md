# Sistema de Gestao Financeira Pessoal

## Tecnologias utilizadas

- Python
- Django
- PostgreSQL
- HTML, CSS e JavaScript
- Chart.js e BootStrap

## Requisitos

Antes de rodar o projeto, instale:

- Python 3.12 ou superior
- PostgreSQL
- Git, caso va baixar o projeto pelo repositorio

## Como rodar o sistema apos baixar

### 1. Acesse a pasta do projeto

```bash
cd Projeto_GF
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

### 3. Instale as dependencias

```bash
pip install -r requirements.txt
```

Caso apareca erro relacionado a `dotenv` ou PostgreSQL, instale tambem:

```bash
pip install python-dotenv psycopg2-binary
```

### 4. Configure o arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env` com as informacoes do banco:

```env
SECRET_KEY=sua_chave_secreta
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=localhost
DB_PORT=5432
```

Para recuperacao de senha por e-mail, tambem podem ser adicionadas:

```env
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
```

Se essas variaveis de e-mail nao forem configuradas, o Django exibira os links de recuperacao de senha no terminal.

### 5. Crie o banco no PostgreSQL

Crie um banco com o mesmo nome informado em `DB_NAME`.

Exemplo:

```sql
CREATE DATABASE nome_do_banco;
```

### 6. Execute as migracoes

```bash
python manage.py migrate
```

### 7. Crie um superusuario

```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor

```bash
python manage.py runserver
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Acesso ao admin

O painel administrativo pode ser acessado em:

```text
http://127.0.0.1:8000/admin/
```

Use o superusuario criado no passo anterior.

## Gerar dados de teste

O projeto possui um comando para gerar registros aleatorios:

```bash
python manage.py gerar_1000_registros
```

Observacao: esse comando esta configurado para buscar um usuario especifico pelo ID. Se necessario, altere o ID dentro do arquivo:

```text
financeiro/management/commands/gerar_1000_registros.py
```

