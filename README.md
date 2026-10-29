# Catálogo de Filmes

Sistema CRUD desenvolvido com Python, Flask, SQLite, HTML e Jinja2 para a atividade prática da UC32.

## Funcionalidades

- Cadastrar filmes com título, gênero, ano e nota de 1 a 10.
- Listar os filmes cadastrados.
- Editar os dados de um filme.
- Excluir filmes.
- Criar automaticamente o banco de dados SQLite.

## Requisitos

- Python 3.10 ou superior
- pip

## Executar localmente

1. Abra um terminal na pasta do projeto.
2. (Opcional, recomendado) Crie e ative um ambiente virtual:

   Windows:
   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o sistema:

   ```bash
   python app.py
   ```

5. Abra http://127.0.0.1:5000 no navegador.

O arquivo `instance/catalogo.db` é criado automaticamente. A pasta `instance` não é enviada ao GitHub.

## Publicar no GitHub

Crie um repositório vazio no GitHub. Na pasta do projeto, execute:

```bash
git init
git add .
git commit -m "Cria catálogo de filmes"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

Substitua a URL de exemplo pela URL do seu repositório.

## Publicar no Render

1. Entre no Render e selecione **New → Web Service**.
2. Conecte o repositório do GitHub.
3. Use estas configurações:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Escolha o plano disponível para seu uso e clique em **Deploy Web Service**.

## Observação sobre SQLite no Render

Em serviços sem disco persistente, o banco SQLite pode ser perdido durante uma nova implantação ou reinicialização. Para um projeto de estudo isso pode ser aceitável. Para preservar os dados, seria necessário configurar um disco persistente ou usar um banco de dados gerenciado, como PostgreSQL.
