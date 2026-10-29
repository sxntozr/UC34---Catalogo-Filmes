import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-dev-catalogo-filmes")

# O banco fica na pasta instance, criada automaticamente.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)
DATABASE = os.path.join(INSTANCE_DIR, "catalogo.db")


def get_db():
    """Abre uma conexão SQLite por requisição."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """Fecha a conexão ao terminar a requisição."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria a tabela automaticamente se ela ainda não existir."""
    connection = sqlite3.connect(DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota REAL NOT NULL CHECK (nota >= 1 AND nota <= 10)
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def index():
    db = get_db()
    filmes = db.execute(
        "SELECT id, titulo, genero, ano, nota FROM filmes ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", filmes=filmes)


@app.route("/novo", methods=["GET", "POST"])
def novo_filme():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_texto = request.form.get("ano", "").strip()
        nota_texto = request.form.get("nota", "").strip().replace(",", ".")

        erro = validar_filme(titulo, genero, ano_texto, nota_texto)
        if erro:
            flash(erro, "erro")
            return render_template("form.html", filme=request.form, acao="Cadastrar")

        db = get_db()
        db.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, int(ano_texto), float(nota_texto))
        )
        db.commit()
        flash("Filme cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", filme=None, acao="Cadastrar")


@app.route("/editar/<int:filme_id>", methods=["GET", "POST"])
def editar_filme(filme_id):
    db = get_db()
    filme = db.execute(
        "SELECT id, titulo, genero, ano, nota FROM filmes WHERE id = ?",
        (filme_id,)
    ).fetchone()

    if filme is None:
        flash("Filme não encontrado.", "erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_texto = request.form.get("ano", "").strip()
        nota_texto = request.form.get("nota", "").strip().replace(",", ".")

        erro = validar_filme(titulo, genero, ano_texto, nota_texto)
        if erro:
            flash(erro, "erro")
            return render_template("form.html", filme=request.form, acao="Salvar alterações")

        db.execute(
            """UPDATE filmes
               SET titulo = ?, genero = ?, ano = ?, nota = ?
               WHERE id = ?""",
            (titulo, genero, int(ano_texto), float(nota_texto), filme_id)
        )
        db.commit()
        flash("Filme atualizado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", filme=filme, acao="Salvar alterações")


@app.route("/excluir/<int:filme_id>", methods=["POST"])
def excluir_filme(filme_id):
    db = get_db()
    resultado = db.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
    db.commit()

    if resultado.rowcount:
        flash("Filme excluído com sucesso.", "sucesso")
    else:
        flash("Filme não encontrado.", "erro")

    return redirect(url_for("index"))


def validar_filme(titulo, genero, ano_texto, nota_texto):
    if not titulo or not genero or not ano_texto or not nota_texto:
        return "Preencha todos os campos."

    try:
        ano = int(ano_texto)
    except ValueError:
        return "Informe um ano válido."

    if ano < 1888 or ano > 2100:
        return "Informe um ano entre 1888 e 2100."

    try:
        nota = float(nota_texto)
    except ValueError:
        return "A nota deve ser um número entre 1 e 10."

    if not 1 <= nota <= 10:
        return "A nota deve estar entre 1 e 10."

    return None


# Cria o banco ao iniciar o aplicativo.
init_db()

if __name__ == "__main__":
    app.run(debug=True)
